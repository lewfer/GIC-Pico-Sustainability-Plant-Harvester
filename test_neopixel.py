# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
NeoPixel example for Pico. Turns the NeoPixels red.

REQUIRED HARDWARE:
* RGB NeoPixel LEDs connected to pin GP0.
"""
import board
import neopixel
from harvest_gpio import *
from time import sleep

# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 30

pixels = neopixel.NeoPixel(PIN_NEOPIXEL, num_pixels)
pixels.brightness = 1

while True:
    pixels.fill((255, 0, 0))
    sleep(1)
    pixels.fill((0, 255, 0))
    sleep(1)
    pixels.fill((0, 0, 255))
    sleep(1)