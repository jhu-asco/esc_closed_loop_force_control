# Test controller for force control
# from  load cell
# Written by: Joseph Chung under ASCOL
# Email: jchung55@jhu.edu
# Modified by Gowtham Garimella (ggarime1@jhu.edu)
# Date: 7/12/17

import time
import matplotlib.pyplot as plt
import numpy as np
from phidget_bridge import PhidgetBridge
from arduino_communication import ArduinoCommunication
from control_loop import ControlLoop

# Specifies the frequency at which the PhidgetBridge will take in data
frequency = 50
# Time interval between force data collection points
time_off = (1.0 / frequency)
# For how much time to run the controller
tf = 10.0
# Cutoff frequency for low pass filter
cutoff = 10.0
# Desired Force (N)
desired_force = 2.0
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
arduino_communication = ArduinoCommunication(port='/dev/ttyACM0', baud_rate=115200)

# Control Loop
control_loop = ControlLoop(cutoff, frequency)

# Low pass filter

# Set desired force
control_loop.setDesiredForce(desired_force)

# Store filtered and unfiltered force lists, Commanded PWM
unfiltered_force = []
filtered_force = []
commanded_pwm = []
try:
    t_init = time.time()
    # While running for tf time controls the motor
    print "Starting control loop"
    while (time.time() - t_init) < tf:
        unfiltered_force.append(phidget_bridge.getForce())
        commanded_pwm.append(control_loop(unfiltered_force[-1]))
        filtered_force.append(control_loop.filtered_force)
        arduino_communication.sendMotorCommandToArduino(commanded_pwm[-1])
        if abs(time.time() - t_init - 5) < 0.1:
            print "5 seconds up"
        time.sleep(time_off)
finally:
    print "Sending 0 to Arduino"
    arduino_communication.sendMotorCommandToArduino(0)
# Closes the PhidgetBridge connection
phidget_bridge.close()
# Plot filtered and unfilt force and desired force
plt.ion()
plt.figure(1)
ts = np.arange(len(filtered_force)) * time_off
plt.plot(ts, filtered_force, 'b')
plt.plot(ts, unfiltered_force, 'r')
plt.plot([ts[0], ts[-1]], [desired_force, desired_force], 'm--')
plt.xlabel('Time(sec)')
plt.ylabel('Force(N)')
plt.legend(['Filtered force', 'Unfiltered force', 'Desired Force'])
plt.figure(2)
plt.plot(ts, commanded_pwm, 'b')
plt.xlabel('Time(sec)')
plt.ylabel('Commanded PWM(%)')
# Wait for plot to be closed
plt.show(block=True)
