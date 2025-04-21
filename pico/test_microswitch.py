# Test the microswitches

import board
import time
from digitalio import DigitalInOut, Direction, Pull
from harvest_gpio import *

# Microswitches for belt drive
rearSwitch = DigitalInOut(board.GP21)
rearSwitch.direction = Direction.INPUT
rearSwitch.pull = Pull.UP  
frontSwitch = DigitalInOut(board.GP20)
frontSwitch.direction = Direction.INPUT
frontSwitch.pull = Pull.UP

while True:
    print("Front", frontSwitch.value, "Rear", rearSwitch.value)
    time.sleep(1)