#!/usr/bin/env python2
"""
Created on Wed Jul 12 20:46:52 2017

Feedback controller to udate force based on PWM

@author: gowtham
"""


class FirstOrderFeedbackController:
    """
    First order P Controller
    """

    def __init__(self, force_pwm_gain=1, user_pwm_gain=1):
        """
        Constructor. Creates initial settings

        Parameters:
        force_pwm_gain -- The slope of steady state force vs pwm(%)
                          curve.
        user_pwm_gain  -- The user specified gain on how quickly the
                          force should converge to the desired force
        """
        # Check inputs are ok
        assert(force_pwm_gain > 0.01)
        assert(user_pwm_gain > 0)
        # Feedforward gain between force and pwm
        self.force_pwm_gain = force_pwm_gain
        # How fast the user wants the force to reach desired force
        self.user_pwm_gain = user_pwm_gain

    def setForcePWMGain(self, force_pwm_gain):
        """
        Set the steady state force vs pwm gain, if it is updated
        based on estimator
        Parameters: 
        force_pwm_gain -- The slope of steady state force vs pwm(%)
                          curve.
        """
        self.force_pwm_gain = max(force_pwm_gain, 0.01)

    def control(self, desired_force, estimated_force):
        """
        Control loop to compute the pwm(%) to send to motors
        to acheive a desired force.
        Parameters:
        desired_force -- Desired force to acheive
        estimated_force -- Filtered force that is current force

        Returns: The derivative of pwm(%) to send to motors
        """
        error = (estimated_force - desired_force)
        pwm_out = -(self.user_pwm_gain / self.force_pwm_gain) * (error)
        return pwm_out
