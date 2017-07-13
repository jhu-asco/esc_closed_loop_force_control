#!/usr/bin/env python2
"""
Created on Wed Jul 12 20:46:52 2017

Feedback controller to udate force based on PWM

@author: gowtham
"""

class FirstOrderFeedbackController:
    def __init__(self, force_pwm_gain=1, user_pwm_gain=1):
        # Check inputs are ok
        assert(force_pwm_gain > 0.01)
        assert(user_pwm_gain > 0)
        # Feedforward gain between force and pwm
        self.force_pwm_gain = force_pwm_gain

        # How fast the user wants the force to reach desired force
        self.user_pwm_gain = user_pwm_gain

    def setForcePWMGain(self, force_pwm_gain):
        self.force_pwm_gain = max(force_pwm_gain, 0.01)

    def control(self, desired_force, estimated_force):
        error = (estimated_force - desired_force)
        pwm_out = -(self.user_pwm_gain/self.force_pwm_gain)*(error)
        return pwm_out
