# Import libraries we need
from harvest_lib import *

# Number of steps to take on each movement
STEPS = 50

# Set it to move forwards
direction = "F"

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
        print("Hit switch F")
        direction = "B"
        noChop()   # we can't chop on the backwards movement
    elif backSwitchHit():
        # Start moving forwards
        print("Hit switch B")
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
