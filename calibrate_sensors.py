# Plant harvester completed code

# Import libraries we need
import board
import time
from harvest_lib import *


# Loop forever
while True:
        
    # Check the sensors
    colour = readColour()
    light = readLight()
    moisture = readMoisture()
    print("Colour:", colour, "Light:", light, "Moisture:", moisture)
    
    time.sleep(0.2)
    

    
    






