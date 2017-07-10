import time
from phidget_bridge import PhidgetBridge

i = 0
# Specifies the frequency at which the PhidgetBridge will take in data
frequency = 10
time_off = 0.1
# Calls class with a specified frequency
phidget_bridge = PhidgetBridge(frequency)
# Calls function to wait for connection
phidget_bridge.waitingForConnection(timeout = 5000)
# While iterating 10 times, prints the force and sleeps for a specified time
while i < 10:
    print(phidget_bridge.getForce())
    time.sleep(time_off)
    i += 1
# Closes the PhidgetBridge connection
phidget_bridge.close()

