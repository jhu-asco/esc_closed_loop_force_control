# Test for Force Filter: Plot filtered and actual force data
# from  load cell
# Written by: Joseph Chung under ASCOL
# Email: jchung55@jhu.edu
# Modified by Gowtham Garimella (ggarime1@jhu.edu)
# Date: 7/12/17

import time
import numpy as np
import argparse
import matplotlib.pyplot as plt
from phidget_bridge import PhidgetBridge
from online_low_pass_filter import OnlineButterLowPassFilter
from arduino_communication import ArduinoCommunication

# Get arguments from commandline
parser = argparse.ArgumentParser(description='Test arduino communication.')
parser.add_argument('-p', '--port', type=str, help='Serial port', default='COM6')
parser.add_argument('-c', '--cutoff', type=float,
                    help='Cutoff frequency for filtering', default=3.0)
parser.add_argument('--pwm', type=float,
                    help='PWM percentage to send to motor', default=20.0)
args = parser.parse_args()
# Specifies the frequency at which the PhidgetBridge will take in data
frequency = 50
# Time interval between force data collection points
time_off = 0.02
# PWM percentage to send to motors
percentage = args.pwm
# For how much time to run the filtering
tf = 5.0
# Cutoff frequency for low pass filter
cutoff = args.cutoff
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
arduino_communication = ArduinoCommunication(port=args.port, baud_rate=115200)
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
