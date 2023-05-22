# Plant harvester completed code

# Import libraries we need
from harvest_lib import *

# Set thresholds at which sensors trigger
#setMoistureThreshold(40)
#setLightThreshold(70)

# Move platform all the way back
#moveFullBack()

# Set it to move forwards
direction = "F"

# Number of steps to take on each movement
STEPS = 50

# Loop forever
while True:
    # Allow our plant to grow 
    grow()
    
    # Move the platform forwards or backwards
    if direction=="F":
        forward(STEPS)
    else:
        backward(STEPS)
    
    # Change direction if a switch hit (False if hit, True if not hit)
    if frontSwitchHit():
        # Start moving backwards
        print("Hit switch B")
        direction = "B"
        noChop()   # we can't chop on the backwards movement
    elif backSwitchHit():
        # Start moving forwards
        print("Hit switch F")
        direction = "F"
        
    # Check the sensors
    red,green,blue = readColour()
    light = readLight()
    moisture = readMoisture()
    print("Colour:", red,green,blue, "Light:", light, "Moisture:", moisture)
    
    # If fruit is ripe, harvest
    if direction == "F" and red>70:
        print("Chop")
        chop(5)
        
        
    
    





