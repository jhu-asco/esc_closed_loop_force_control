#!/usr/bin/env python2
"""
Created on Wed Jul 12 20:46:52 2017

Integral Feedback controller to update force based on PWM

@author: gowtham
"""

import numpy as np

class IntegralFeedbackController:
    """
    First order P Controller
    """

    def __init__(self, max_pwm_change, dt, integral_pwm_gain=1, force_pwm_gain=1):
        """
        Constructor. Creates initial settings

        Parameters:
        max_pwm_change -- The maximum pwm change in a given cycle
        dt -- change in time over the integration
        force_pwm_gain -- The slope of steady state force vs pwm(%)
                          curve.
        integral_pwm_gain  -- The user specified gain on how quickly the
                          force should converge to the desired force
        """
        # Check inputs are ok
        assert(force_pwm_gain > 0.01)
        assert(integral_pwm_gain > 0)
        # Feedforward gain between force and pwm
        self.force_pwm_gain = force_pwm_gain
        # How fast the user wants the force to reach desired force
        self.integral_pwm_gain = integral_pwm_gain
        # Initializes the integral value as zero
        self.integral_out = 0
        # Intializes the max_pwm_change to the passed in value for the class
        self.max_pwm_change = max_pwm_change        
        # Intializes the dt to the passed in value for the class
        self.dt = dt        

    def setForcePWMGain(self, force_pwm_gain):
        """
        Set the steady state force vs pwm gain, if it is updated
        based on estimator
        Parameters: 
        force_pwm_gain -- The slope of steady state force vs pwm(%)
                          curve.
        """
        self.force_pwm_gain = max(force_pwm_gain, 0.01)

    def control(self, error):
        """
        Control loop to compute the integral portion for the motors
        to acheive a desired force.
        Parameters:
        Error -- Difference between filtered force and desired force

        Returns: The pwm(%) to send to motors
        """
        # Computes PWM from the error
        pwm = -(self.integral_pwm_gain / self.force_pwm_gain) * (error) * (self.dt)
        # Clips the integral value between the max and min pwm values
        self.integral_out += np.clip(pwm, -self.max_pwm_change, self.max_pwm_change)
        return self.integral_out
