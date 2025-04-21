# Test the stepper

import time
import board
import digitalio
from harvest_gpio import *

pins = [
    digitalio.DigitalInOut(PIN_STEPPER_1),
    digitalio.DigitalInOut(PIN_STEPPER_2),
    digitalio.DigitalInOut(PIN_STEPPER_3),
    digitalio.DigitalInOut(PIN_STEPPER_4)
]


pins[0].direction = digitalio.Direction.OUTPUT
pins[1].direction = digitalio.Direction.OUTPUT
pins[2].direction = digitalio.Direction.OUTPUT
pins[3].direction = digitalio.Direction.OUTPUT

#one hot encoding vectors
full_step_sequence = [
    [1,1,0,0],
    [0,1,1,0],
    [0,0,1,1],
    [1,0,0,1]
]

numSteps = 300          # higher means more distance travelled
rpm = 12 				# rpm - set to 1 to 15
stepsperrot = 2048      # steps per rotation - don't change (

for i in range(numSteps):
    for step in full_step_sequence:
        for i in range(len(pins)):
            pins[i].value = step[i]
        #time.sleep(0.002)
        time.sleep(60 / (rpm * stepsperrot))

for i in range(numSteps):
    for step in reversed(full_step_sequence):
        for i in range(len(pins)):
            pins[i].value = step[i]
        time.sleep(60 / (rpm * stepsperrot))