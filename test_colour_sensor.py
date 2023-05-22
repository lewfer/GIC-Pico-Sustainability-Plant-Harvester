# Test the colour sensor

import board
import adafruit_tcs34725
import busio
import time
from harvest_gpio import *

i2c = busio.I2C(PIN_COLOUR_SCL, PIN_COLOUR_SDA)
sensor = adafruit_tcs34725.TCS34725(i2c)

while True:
    print('Color: ({0}, {1}, {2})'.format(*sensor.color_rgb_bytes))
    print('Temperature: {0}K'.format(sensor.color_temperature))
    print('Lux: {0}'.format(sensor.lux))
    time.sleep(0.5)
