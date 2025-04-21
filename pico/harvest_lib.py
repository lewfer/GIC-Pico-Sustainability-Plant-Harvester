import board
import neopixel
import time
import digitalio
import analogio
import adafruit_tcs34725
import busio
import pwmio
from adafruit_motor import servo
#from digitalio import DigitalInOut, Direction, Pull
import random
from harvest_gpio import *

# Set up components

# Neopixel
num_pixels = 5
pixels = neopixel.NeoPixel(PIN_NEOPIXEL, num_pixels)
pixels.brightness = 0

# Colour sensor
i2c = busio.I2C(PIN_COLOUR_SCL, PIN_COLOUR_SDA)
colourSensor = adafruit_tcs34725.TCS34725(i2c)

# Servo setup
pwm_servo = pwmio.PWMOut(PIN_SERVO, duty_cycle=2 ** 15, frequency=50)
servo1 = servo.Servo(
    pwm_servo, min_pulse=500, max_pulse=2200
)  # tune pulse for specific servo
servo1.angle = 90

# Stepper
STEPPER_RPM = 6 				# rpm - set to 1 to 15
STEPPER_STEPS_PER_ROT = 2048    # steps per rotation - don't change (

stepperPins = [
    digitalio.DigitalInOut(PIN_STEPPER_1),
    digitalio.DigitalInOut(PIN_STEPPER_2),
    digitalio.DigitalInOut(PIN_STEPPER_3),
    digitalio.DigitalInOut(PIN_STEPPER_4)
]
stepperPins[0].direction = digitalio.Direction.OUTPUT
stepperPins[1].direction = digitalio.Direction.OUTPUT
stepperPins[2].direction = digitalio.Direction.OUTPUT
stepperPins[3].direction = digitalio.Direction.OUTPUT

#one hot encoding vectors
full_step_sequence = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]
]

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set initial fruit colours
pixels[0] = GREEN
pixels[1] = GREEN
pixels[2] = GREEN
pixels[3] = GREEN
pixels[4] = GREEN

# Microswitches for belt drive
backSwitch = digitalio.DigitalInOut(PIN_BACKSWITCH)
backSwitch.direction = digitalio.Direction.INPUT
backSwitch.pull = digitalio.Pull.UP  
frontSwitch = digitalio.DigitalInOut(PIN_FRONTSWITCH)
frontSwitch.direction = digitalio.Direction.INPUT
frontSwitch.pull = digitalio.Pull.UP

# Sensors
lightSensor = analogio.AnalogIn(PIN_LIGHTSENSOR)
moistureSensor = analogio.AnalogIn(PIN_MOISTURESENSOR)


# fruit
fruitRipeness = [0,0,0]

# Speed at which fruit ripens
# Shuffle these numbers so random fruits mature at different rates
randomAgeing = [5,10,20]
fruitRandom = []
for i in range(3):
    n = random.randint(0,2-i)
    fruitRandom.append(randomAgeing[n])
    randomAgeing.remove(randomAgeing[n])
print(fruitRandom)
#fruitRandom = [5, 10, 20]

# Thresholds
MOISTURE_THRESHOLD = 40
LIGHT_THRESHOLD = 70

tick = 0
chopTick = 0
chopCount = 3

# API

# Set brighness 0 to 1
def setBrightness(amount):
    pixels.brightness = amount

def setColour(pixel, colour):
    pixels[pixel] = colour


    
# Fruit ripeness will go from 0 to 255, which is the ripening phase (green to red)
# then from 255 to 512, which is the rotting phase  (red to blue)
def grow():
    global tick
    
    #print(fruitRipeness)
    
    #print(MOISTURE_THRESHOLD)
    moisture = readMoisture()
    light = readLight()
        
    if moisture<MOISTURE_THRESHOLD:
        # No moisture, turn off
        #pixels[i] = (0,0,0)
        pixels.brightness = moisture/MOISTURE_THRESHOLD
    else:
        pixels.brightness = 1
        print("Growing", end="")
        if light>LIGHT_THRESHOLD:
            print(" and ripening", end="")
        for i in range(3):
            
            # If enough light
            if light>LIGHT_THRESHOLD:
                # Compute new ripeness level
                
                # If already fully ripe, start rotting
                if fruitRipeness[i]>=255:
                    fruitRipeness[i] += int(random.randint(0,9)/1) # rot slowly
                    
                # Ripen 
                if fruitRipeness[i]<255:
                    fruitRipeness[i] += random.randint(0,fruitRandom[i]) # ripen quickly                    
            
            # Show colour according to fruit state
            if fruitRipeness[i]<256:
                # Ripening
                pixels[i] = (fruitRipeness[i], 255-fruitRipeness[i], 0) # more red, less green as fruitRipeness increases
            elif fruitRipeness[i]<512:
                # Rotting
                pixels[i] = (255-(fruitRipeness[i]-255), 0, fruitRipeness[i]-256) # less red, more blue as fruitRipeness increases
        print("")
                
    tick += 1
    
    if tick-chopTick > chopCount:
        noChop()
    #print("Ripeness:",fruitRipeness)
        
    
def setSpeed(speed):
    global STEPPER_RPM
    STEPPER_RPM = speed
    
    
def forward(numSteps):
    for i in range(numSteps):
        for step in reversed(full_step_sequence):
            for i in range(len(stepperPins)):
                stepperPins[i].value = step[i]
            time.sleep(60 / (STEPPER_RPM * STEPPER_STEPS_PER_ROT))
                
def backward(numSteps):
    for i in range(numSteps):
        for step in full_step_sequence:
            for i in range(len(stepperPins)):
                stepperPins[i].value = step[i]
            time.sleep(60 / (STEPPER_RPM * STEPPER_STEPS_PER_ROT))

def moveFullBack():
    while backSwitch.value:
        print(backSwitch.value)
        backward(100)
        time.sleep(0.05)
        
        
def moveFullForward():
    while frontSwitch.value:
        print(frontSwitch.value)
        forward(100)
        time.sleep(0.05)
    
def readColour():
#     print('Color: ({0}, {1}, {2})'.format(*colourSensor.color_rgb_bytes))
#     print('Temperature: {0}K'.format(colourSensor.color_temperature))
#     print('Lux: {0}'.format(colourSensor.lux))
    return colourSensor.color_rgb_bytes

def readLight():
    return round(lightSensor.value * 100 / 65535)

def readMoisture():
    return round((65535-moistureSensor.value) * 100 / 65535)

def setMoistureThreshold(t):
    global MOISTURE_THRESHOLD
    MOISTURE_THRESHOLD = t
    
def setLightThreshold(t):
    global LIGHT_THRESHOLD
    LIGHT_THRESHOLD = t
    

def chopForward(count=1):
    global chopTick
    global chopCount
    
    servo1.angle = 20
    chopTick = tick
    chopCount = count

def chopBackward(count=1):
    global chopTick
    global chopCount
    
    servo1.angle = 160
    chopTick = tick
    chopCount = count
    
def noChop():
    servo1.angle = 90    
    
def frontSwitchHit():
    return frontSwitch.value==False

def backSwitchHit():
    return backSwitch.value==False

