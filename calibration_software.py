import time
from phidget_bridge import PhidgetBridge

frequency = 10
phidget_bridge = PhidgetBridge(frequency)

try:
    phidget_bridge.waitingForConnection() 
except:
    print "Phidget Bridge is not connected"
    exit(0)
if not phidget_bridge.connected_status:
    print "Phidget Bridge is not connected"
    exit(0)

t_end = time.time() + 2
while time.time() < t_end:
    force = phidget_bridge.getForce()
    mass = force/phidget_bridge.gravity
    voltage = mass/phidget_bridge.force_scaling
    print("Mass: %f, Voltage: %f " % (mass, voltage))
    time.sleep(1.0/frequency)