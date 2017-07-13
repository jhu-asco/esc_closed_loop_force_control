# Test for Force Filter: Plot filtered and actual force data
# from  load cell
# Written by: Joseph Chung under ASCOL
# Email: jchung55@jhu.edu
# Modified by Gowtham Garimella (ggarime1@jhu.edu)
# Date: 7/12/17

import time
import numpy as np
from phidget_bridge import PhidgetBridge
from online_low_pass_filter import OnlineButterLowPassFilter
from arduino_communication import ArduinoCommunication
import matplotlib.pyplot as plt

# Specifies the frequency at which the PhidgetBridge will take in data
frequency = 50
# Time interval between force data collection points
time_off = 0.02
# PWM percentage to send to motors
percentage = 20
# For how much time to run the filtering
tf = 5.0
# Cutoff frequency for low pass filter
cutoff = 3.0
# Calls class with a specified frequency
phidget_bridge = PhidgetBridge(frequency)
# Calls function to wait for connection
phidget_bridge.waitingForConnection(timeout=5000)
# Checks if the Phidget Bridge is connected; if not, exits program
try:
    phidget_bridge.waitingForConnection()
except:
    print "Phidget Bridge is not connected"
    exit(0)
if not phidget_bridge.connected_status:
    print "Phidget Bridge is not connected"
    exit(0)

# Connect arduino
# Include arduino-related functions
arduino_communication = ArduinoCommunication(port='/dev/ttyACM0')
# Create a low pass filter
low_pass_filter = OnlineButterLowPassFilter(cutoff, 1.0 / time_off)
# Store filtered and unfiltered force lists
unfiltered_force = []
filtered_force = []
try:
    print "Sending Motor PWM"
    arduino_communication.sendMotorCommandToArduino(percentage)
    t_init = time.time()
    # Iterating for tf seconds, filters and stores force
    while (time.time() - t_init) < tf:
        unfiltered_force.append(phidget_bridge.getForce())
        filtered_force.append(
            low_pass_filter.filterValue(unfiltered_force[-1]))
        time.sleep(time_off)
finally:
    print "Sending 0 PWM"
    arduino_communication.sendMotorCommandToArduino(0)
# Closes the PhidgetBridge connection
phidget_bridge.close()
# Plot filtered and unfilt force
plt.ion()
plt.figure(1)
filtered_force_array = np.array(filtered_force)
ts = np.arange(filtered_force_array.size) * time_off
plt.plot(ts, filtered_force_array, 'b')
plt.plot(ts, unfiltered_force, 'r')
plt.xlabel('Time(sec)')
plt.ylabel('Force(N)')
plt.legend(['Filtered force', 'Unfiltered force'])
# Wait for plot to be closed
plt.show(block=True)
