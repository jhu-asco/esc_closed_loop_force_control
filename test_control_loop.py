# Test controller for force control
# from  load cell
# Written by: Joseph Chung under ASCOL
# Email: jchung55@jhu.edu
# Modified by Gowtham Garimella (ggarime1@jhu.edu)
# Date: 7/12/17

import time
import matplotlib.pyplot as plt
import numpy as np
import argparse
from phidget_bridge import PhidgetBridge
from arduino_communication import ArduinoCommunication
from control_loop import ControlLoop

# Add argument parser to read arguments from command line
parser = argparse.ArgumentParser(description='Test arduino communication.')
parser.add_argument('-p', '--port', type=str, help='Serial port', default='COM6')
parser.add_argument('-f', '--freq', type=float, help='Control and sample frequency',
                    default=50)
parser.add_argument('-t', type=float, help='Time to run control loop for',
                    default=10)
parser.add_argument('-u', '--use_proportional', type=bool, help='Use proportional controller',
                    default=True)
parser.add_argument('-c', '--cutoff', type=float,
                    help='Cutoff frequency for sampling',
                    default=10)
parser.add_argument('-d', '--desired_force',  type=float,
                    help='Desired force in N',
                    default=2.0)
args = parser.parse_args()
# Specifies the frequency at which the PhidgetBridge will take in data
frequency = args.freq
# Time interval between force data collection points
time_off = (1.0 / frequency)
# For how much time to run the controller
tf = args.t
# Cutoff frequency for low pass filter
cutoff = args.cutoff
# Desired Force (N)
desired_force = args.desired_force
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
arduino_communication = ArduinoCommunication(port=args.port,
                                             baud_rate=115200)

# Control Loop
control_loop = ControlLoop(cutoff, frequency, args.use_proportional)

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
