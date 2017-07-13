# Test for the Phidget Bridge: Instantiate and collect force data from load cell
# Written by: Joseph Chung under ASCOL
# Email: jchung55@jhu.edu
# Date: 7/11/17

import time
from phidget_bridge import PhidgetBridge

# Specifies the frequency at which the PhidgetBridge will take in data
frequency = 10
# Time interval between force data collection points
time_off = 0.1
# Calls class with a specified frequency
phidget_bridge = PhidgetBridge(frequency)
# Calls function to wait for connection
phidget_bridge.waitingForConnection(timeout = 5000)
# Checks if the Phidget Bridge is connected; if not, exits program
try:
    phidget_bridge.waitingForConnection() 
except:
    print "Phidget Bridge is not connected"
    exit(0)
if not phidget_bridge.connected_status:
    print "Phidget Bridge is not connected"
    exit(0)
# While iterating 10 times, prints the force and sleeps for a specified time
for i in range(10):
    print(phidget_bridge.getForce())
    time.sleep(time_off)
    i += 1
# Closes the PhidgetBridge connection
phidget_bridge.close()