#!/usr/bin/env python2
import time
import numpy as np
import matplotlib.pyplot as plt
from adaptive_feedback_controller import AdaptiveFeedbackController


# For how much time to run the controller
tf = 100.0
# Frequency of running controller
freq = 100
dt = 1.0/freq
# Desired Force trajectory (N)
dfreq = 0.5
omega = 2*np.pi*dfreq
#omega = 0
amp = 5.0
bias = 2.0

# Initialize estimated force
estimated_force = 0
# Create estimated force gain
estimated_force_gain = 0.1

# Create an adaptive controller
adaptive_controller = AdaptiveFeedbackController(dt,
                                                 adaptive_gain_change_rate=1)
adaptive_controller.setModelForce(estimated_force)

# Create expected adaptive gains
expected_adaptive_gain = (adaptive_controller.user_pwm_gain /
                          estimated_force_gain)

t0 = time.time()
t_relative = time.time() - t0
# Store states, commands
desired_force = []
adaptive_feedback_gain = []
adaptive_reference_gain = []
force = []
model_force = []
commanded_pwm = []
# How long to run controller
N = int(tf*freq)
for i in range(N):
    # Get desired force , derivative
    desired_force.append(bias + amp*np.sin(omega*t_relative))
    desired_force_derivative = omega*amp*np.cos(omega*t_relative)
    # Store estimated force
    force.append(estimated_force)
    model_force.append(adaptive_controller.model_force)
    # Call controller
    commanded_pwm.append(adaptive_controller.control(desired_force[-1],
                                                     estimated_force,
                                                     desired_force_derivative))
    # Store adaptive gains
    adaptive_feedback_gain.append(adaptive_controller.adaptive_feedback_gain)
    adaptive_reference_gain.append(adaptive_controller.adaptive_reference_gain)
    t_relative += dt
    estimated_force += estimated_force_gain*commanded_pwm[-1]*dt

error_model_force = np.array(force) - np.array(model_force)
inv_adaptive_gain_change_rate = 1.0/adaptive_controller.adaptive_gain_change_rate
e_kx_square = np.square(np.array(adaptive_feedback_gain) + expected_adaptive_gain)
e_kr_square = np.square(np.array(adaptive_reference_gain) - expected_adaptive_gain)
lyap = (np.square(error_model_force) +
        estimated_force_gain*(inv_adaptive_gain_change_rate*(e_kx_square +
                                                             e_kr_square)))
# Plot force and desired force
ts = np.arange(len(force)) * dt
plt.ion()
plt.figure(1)
plt.subplot(2,1,1)
plt.plot(ts, force, 'b')
plt.plot(ts, model_force, 'r')
plt.plot(ts, desired_force, 'm--')
plt.ylabel('Force(N)')
plt.legend(['Force', 'Model Force', 'Desired Force'])
plt.subplot(2,1,2)
plt.plot(ts, lyap, 'b')
plt.ylabel('Square Error')
plt.xlabel('Time(sec)')
plt.figure(2)
plt.plot(ts, commanded_pwm, 'b')
plt.xlabel('Time(sec)')
plt.ylabel('Command')
plt.figure(3)
plt.subplot(2,1,1)
plt.plot(ts, adaptive_feedback_gain, 'b')
plt.plot([ts[0],ts[-1]], -1*expected_adaptive_gain*np.ones(2),'m--')
plt.ylabel('Adaptive Feedback Gain')
plt.subplot(2,1,2)
plt.plot(ts, adaptive_reference_gain, 'b')
plt.plot([ts[0],ts[-1]], expected_adaptive_gain*np.ones(2), 'm--')
plt.ylabel('Adaptive Reference Gain')
plt.xlabel('Time(sec)')
# Wait for plot to be closed
plt.show(block=True)
