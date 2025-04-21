# Test the light sensor
import time
import board
import analogio
from harvest_gpio import *

photocell = analogio.AnalogIn(PIN_LIGHTSENSOR)


# Value will be 0 to 65535 (0 for bright, 65535 for dark or vice versa depending on the order of black/red wires)
while True:
    val = photocell.value
    print(val, str(round(val*100/65535)) + "%")
    time.sleep(.2)