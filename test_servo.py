# Test the servo

import time
import board
import pwmio
from adafruit_motor import servo
from harvest_gpio import *

# Servo setup
pwm_servo = pwmio.PWMOut(PIN_SERVO, duty_cycle=2 ** 15, frequency=50)
servo1 = servo.Servo(
    pwm_servo, min_pulse=500, max_pulse=2200
)  # tune pulse for specific servo


# Servo test
def servo_direct_test():
    print("servo test: 90")
    servo1.angle = 90
    time.sleep(2)
    print("servo test: 20")
    servo1.angle = 20
    time.sleep(2)
    print("servo test: 90")
    servo1.angle = 90
    time.sleep(2)
    print("servo test: 160")
    servo1.angle = 160
    time.sleep(2)

servo_direct_test()
servo1.angle = 90
