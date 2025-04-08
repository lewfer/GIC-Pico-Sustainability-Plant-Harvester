from harvest_lib import *
from time import sleep


setSpeed(15)

while True:
    
    if frontSwitchHit():
        forward(10)
    
    if backSwitchHit():
        backward(10)
        
    sleep(0.01)