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
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]
]

smooth_full_step_sequence = [
    [1,0,0,1],
    [1,0,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1]
]

numSteps = 100
for i in range(numSteps):
    for step in full_step_sequence:
        for i in range(len(pins)):
            pins[i].value = step[i]
            time.sleep(0.001)
    
for i in range(numSteps):
    for step in reversed(full_step_sequence):
        for i in range(len(pins)):
            pins[i].value = step[i]
            time.sleep(0.001)
            
for i in range(numSteps):
    for step in smooth_full_step_sequence:
        for i in range(len(pins)):
            pins[i].value = step[i]
            time.sleep(0.001)

for i in range(numSteps):
    for step in reversed(smooth_full_step_sequence):
        for i in range(len(pins)):
            pins[i].value = step[i]
            time.sleep(0.001)
