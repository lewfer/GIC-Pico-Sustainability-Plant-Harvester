# Test the moisture sensor

import time
import board
import analogio
from harvest_gpio import *

photocell = analogio.AnalogIn(PIN_MOISTURESENSOR)


# Value will be 0 to 65535 (65535 is dry)
while True:
    val = photocell.value
    print(val, str(round((65525-val)*100/65535))+"%")
    time.sleep(.2)