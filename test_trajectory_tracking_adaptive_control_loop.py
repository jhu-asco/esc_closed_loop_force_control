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
from adaptive_control_loop import AdaptiveControlLoop

# Add argument parser to read arguments from command line
parser = argparse.ArgumentParser(description='Test arduino communication.')
parser.add_argument('-p', '--port', type=str, help='Serial port', default='COM6')
parser.add_argument('-f', '--freq', type=float, help='Control and sample frequency',
                    default=100)
parser.add_argument('-t', type=float, help='Time to run control loop for',
                    default=10)
parser.add_argument('-c', '--cutoff', type=float,
                    help='Cutoff frequency for sampling',
                    default=20)
parser.add_argument('--dfreq', type=float,
                    help='desired force frequency assuming sinusoid',
                    default=0.1)
parser.add_argument('--damp', type=float,
                    help='desired force amplitude assuming sinusoid',
                    default=0.5)
parser.add_argument('--dbias', type=float,
                    help='desired force bias assuming sinusoid',
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
# Desired Force trajectory (N)
omega = 2*np.pi*args.dfreq
amp = args.damp
bias = args.dbias
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
control_loop = AdaptiveControlLoop(cutoff, frequency)

# Reset Model force
control_loop.resetModelForce(0.0)
# Slope of Force vs pwm curve
expected_force_pwm_gain = 0.118
# Set adaptive gains to something meaningful
expected_adaptive_gain = (control_loop.feedback_controller.user_pwm_gain /
                          expected_force_pwm_gain)
control_loop.feedback_controller.resetAdaptiveGains(expected_adaptive_gain)

# Store filtered and unfiltered force lists, Commanded PWM
desired_force = []
unfiltered_force = []
filtered_force = []
model_force = []
commanded_pwm = []
kx = []
kr = []
try:
    t_init = time.time()
    # While running for tf time controls the motor
    print "Starting control loop"
    t_relative = (time.time() - t_init)
    while  t_relative < tf:
        # Set desired force
        desired_force.append(bias + amp*np.sin(omega*t_relative))
        desired_force_derivative = omega*amp*np.cos(omega*t_relative)
        control_loop.setDesiredForce(desired_force[-1], desired_force_derivative)
        unfiltered_force.append(phidget_bridge.getForce())
        commanded_pwm.append(control_loop(unfiltered_force[-1]))
        filtered_force.append(control_loop.filtered_force)
        model_force.append(control_loop.feedback_controller.model_force)
        kx.append(control_loop.feedback_controller.adaptive_feedback_gain)
        kr.append(control_loop.feedback_controller.adaptive_reference_gain)
        arduino_communication.sendMotorCommandToArduino(commanded_pwm[-1])
        if abs(time.time() - t_init - 5) < 0.1:
            print "5 seconds up"
        time.sleep(time_off)
        t_relative = (time.time() - t_init)
finally:
    print "Sending 0 to Arduino"
    arduino_communication.sendMotorCommandToArduino(0)
# Closes the PhidgetBridge connection
phidget_bridge.close()
# Time samples for plotting
ts = np.arange(len(filtered_force)) * time_off
# Plot filtered and unfilt force and desired force
plt.ion()
plt.figure(1)
plt.plot(ts, filtered_force, 'b')
plt.plot(ts, unfiltered_force, 'r')
plt.plot(ts, model_force, 'k-.')
plt.plot(ts, desired_force, 'm--')
plt.xlabel('Time(sec)')
plt.ylabel('Force(N)')
plt.legend(['Filtered force', 'Unfiltered force', 'Model force',
            'Desired Force'])
plt.figure(2)
plt.plot(ts, commanded_pwm, 'b')
plt.xlabel('Time(sec)')
plt.ylabel('Commanded PWM(%)')
plt.figure(3)
plt.subplot(2,1,1)
plt.plot(ts, kx, 'b')
plt.plot([ts[0],ts[-1]], -1*expected_adaptive_gain*np.ones(2),'m--')
plt.ylabel('Adaptive Feedback Gain')
plt.subplot(2,1,2)
plt.plot(ts, kr, 'b')
plt.plot([ts[0],ts[-1]], expected_adaptive_gain*np.ones(2), 'm--')
plt.ylabel('Adaptive Reference Gain')
plt.xlabel('Time(sec)')
# Wait for plot to be closed
plt.show(block=True)
