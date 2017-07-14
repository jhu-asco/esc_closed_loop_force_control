#!/usr/bin/env python2

import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt('force_vs_pwm.txt', delimiter=',')

# Specify range of pwm to use for linear fitting
# Based on using above 25 we get slope, intercept as [ 0.11881013 -1.59079367]
# and using below 25 we get [ 0.05688103 -0.01634158] for CF prop
idx = data[0, :] > 25
data_to_fit = data[:,idx]

# Fit linear line
z = np.polyfit(data_to_fit[0, :], data_to_fit[1,:], deg=1,
               w=1.0/data_to_fit[2,:])
print "Linear fit params: ", z

# Plot
plt.ion()
plt.figure(1)
plt.errorbar(data_to_fit[0,:], data_to_fit[1,:], yerr=data_to_fit[2,:], fmt='b*-')
plt.plot(data_to_fit[0,:], z[0]*data_to_fit[0,:] + z[1], 'r--')
plt.xlabel('PWM(%)')
plt.ylabel('Force(N)')
plt.legend(['Data', 'Line fit'])


