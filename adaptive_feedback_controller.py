#!/usr/bin/env python2
"""
Created on Wed Jul 12 20:46:52 2017

Feedback controller to udate force based on PWM

@author: gowtham
"""
import numpy as np

class AdaptiveFeedbackController:
    """
    First order P Controller
    """

    def __init__(self, dt, user_pwm_gain=1, adaptive_gain_change_rate=1):
        """
        Constructor. Creates initial settings

        Parameters:
        dt             -- Time period. Inverse of frequency of controller
        user_pwm_gain  -- The user specified gain on how quickly the
                          force should converge to the desired force
        adaptive_gain_change_rate -- How quickly to change adaptive gains
        """
        # Check inputs are ok
        assert(dt > 0)
        assert(user_pwm_gain > 0)
        # How fast the user wants the force to reach desired force
        self.user_pwm_gain = user_pwm_gain
        # Initialize model force to zero
        self.model_force = 0
        # Initialize adaptive gains
        self.resetAdaptiveGains()
        #Minimum value the gains can get to
        self.min_adaptive_gain = 0.02
        #Maximum value the gains can get to
        self.max_adaptive_gain = 60
        # Gain on how fast to change adaptive gains
        self.adaptive_gain_change_rate = adaptive_gain_change_rate
        self.dt = dt

    def resetAdaptiveGains(self, adaptive_gain=1.0):
        if adaptive_gain <= 0:
            raise ValueError("Adaptive gain should be greater than 0")
        self.adaptive_feedback_gain = -adaptive_gain
        self.adaptive_reference_gain = adaptive_gain

    def setModelForce(self, input_force):
        self.model_force = input_force

    def updateModelForce(self, reference):
        model_force_dot = -self.user_pwm_gain*(self.model_force - reference)
        self.model_force += model_force_dot*self.dt

    def updateAdaptiveGains(self, error, reference, estimated_force):
        adaptive_feedback_gain_dot = -(self.adaptive_gain_change_rate *
                                       estimated_force *
                                       error)

        adaptive_reference_gain_dot = -(self.adaptive_gain_change_rate *
                                        reference *
                                        error)
        updated_adaptive_feedback = (self.adaptive_feedback_gain +
                                     adaptive_feedback_gain_dot*self.dt)
        self.adaptive_feedback_gain = np.clip(updated_adaptive_feedback,
                                              -self.max_adaptive_gain,
                                              -self.min_adaptive_gain)
        updated_adaptive_reference = (self.adaptive_reference_gain +
                                      adaptive_reference_gain_dot*self.dt)
        self.adaptive_reference_gain = np.clip(updated_adaptive_reference,
                                               self.min_adaptive_gain,
                                               self.max_adaptive_gain)
                                          


    def control(self, desired_force, estimated_force,
                desired_force_derivative=0):
        """
        Control loop to compute the pwm(%) to send to motors
        to acheive a desired force.
        Parameters:
        desired_force -- Desired force to acheive
        estimated_force -- Filtered force that is current force

        Returns: The derivative of pwm(%) to send to motors
        """
        reference = (desired_force +
                     (1.0/self.user_pwm_gain)*desired_force_derivative)
        error = (estimated_force - self.model_force)
        self.updateAdaptiveGains(error, reference, estimated_force)
        self.updateModelForce(reference)
        pwm_dot_out = (self.adaptive_feedback_gain*estimated_force +
                       self.adaptive_reference_gain*reference)
        return pwm_dot_out
