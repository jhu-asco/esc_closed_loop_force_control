# Calibration Information:
# ----------------------------------------------------------------------------
# This software is used to calibrate the (0-5 kg) micro load cell from Phidgets.

# Laying the load cell horizontally above a desk, run this program with no 
# additional mass attached; the resulting mass and voltage values will be your 
# first point of interest.

# For the second point of interest, while keeping the same setup, attach a 
# known mass/weight and run the program again.

# Plot the resulting values in excel and determine a linear equation (y = mx +b)
# where y is your voltage and x is your mass; your m will be your scaling term
# and your b will be your offset.

# For additional information, see URL - 
# https://www.phidgets.com/?tier=3&catid=2&pcid=1&prodid=35#How_to_Calibrate_the_Bridge

import time
from phidget_bridge import PhidgetBridge

frequency = 10 # Set the frequency of data collection
time_on = 2 # Set the time on to 2 seconds 
phidget_bridge = PhidgetBridge(frequency)

# Check if the PhidgetBridge is connected; if not, exit the program
try:
    phidget_bridge.waitingForConnection() 
except:
    print "Phidget Bridge is not connected"
    exit(0)
if not phidget_bridge.connected_status:
    print "Phidget Bridge is not connected"
    exit(0)

# For the time on, gather force data from the bridge, convert to mass and 
# voltage, and print the values while sleeping for set time based on freq.
t_end = time.time() + time_on
while time.time() < t_end:
    force = phidget_bridge.getForce()
    mass = force/phidget_bridge.gravity
    voltage = mass/phidget_bridge.force_scaling
    print("Mass: %f, Voltage: %f " % (mass, voltage))
    time.sleep(1.0/frequency)