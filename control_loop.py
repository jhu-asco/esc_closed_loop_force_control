from first_order_feedback_controller import FirstOrderFeedbackController
from online_low_pass_filter import OnlineButterLowPassFilter
import numpy as np


class ControlLoop:
    """
    Helper class that combines filtering, and calling control loop
    """

    def __init__(self, cutoff, frequency):
        """
        Constructor. Creates filter, controller and initial settings
        Parameters:
        cutoff -- Filter cutoff frequency for filtering force
        frequency -- Sampling frequency for force
        """
        self.force_filter = OnlineButterLowPassFilter(cutoff, frequency)
        self.feedback_controller = FirstOrderFeedbackController(user_pwm_gain=2)
        # For now not implemented adaptive gain estimator
        self.min_pwm = 6 # Enough to keep the motors moving
        self.pwm = self.min_pwm  # Start with minimal PWM percentage
        self.max_pwm = 80 # Max pwm percentage to send
        self.max_pwm_change = 2.0  # How much it can change in 1 cycle
        self.desired_force = 0
        self.desired_force_derivative = 0
        self.filtered_force = 0
        self.dt = (1.0 / frequency)

    def setDesiredForce(self, desired_force, desired_force_derivative=0):
        """
        Desired force (%) for controller
        """
        self.desired_force = desired_force
        self.desired_force_derivative = desired_force_derivative

    def __call__(self, force):
        """
        Main call that takes in a measured force, filters it,
        runs the control loop, integrates and outputs the
        pwm(%) to send to motors
        """
        if force > 15.0 or force < -10:
            print "Warning crazy force reported: %2.3f !"%(force,)
            return
        self.filtered_force = self.force_filter.filterValue(force)
        pwm_dot = self.feedback_controller.control(self.desired_force,
                                                   self.filtered_force,
                                                   self.desired_force_derivative)
        delta_pwm = np.clip(pwm_dot * self.dt, -self.max_pwm_change, self.max_pwm_change)
        self.pwm = np.clip(self.pwm + delta_pwm, self.min_pwm, self.max_pwm)
        return self.pwm
