from proportional_feedback_controller import ProportionalFeedbackController
from integral_feedback_controller import IntegralFeedbackController
from online_low_pass_filter import OnlineButterLowPassFilter
import numpy as np


class ControlLoop:
    """
    Helper class that combines filtering, and calling control loop
    """

    def __init__(self, cutoff, frequency, use_proportional_control = True):
        """
        Constructor. Creates filter, controller and initial settings
        Parameters:
        cutoff -- Filter cutoff frequency for filtering force
        frequency -- Sampling frequency for force
        """
        
        # For now not implemented adaptive gain estimator
        self.min_pwm = 6 # Enough to keep the motors moving
        self.pwm = self.min_pwm  # Start with minimal PWM percentage
        self.max_pwm = 80 # Max pwm percentage to send
        self.max_pwm_change = 1.0  # How much it can change in 1 cycle
        self.desired_force = 0
        self.filtered_force = 0
        self.use_proportional_control = use_proportional_control
        self.error = 0
        self.dt = (1.0 / frequency)
        
        self.force_filter = OnlineButterLowPassFilter(cutoff, frequency)
        self.proportional_feedback_controller = ProportionalFeedbackController(proportional_pwm_gain = 10)
        self.integral_feedback_controller = IntegralFeedbackController(self.max_pwm_change, self.dt, integral_pwm_gain=15.0, force_pwm_gain = 1)

    def setDesiredForce(self, desired_force):
        """
        Desired force (%) for controller
        """
        self.desired_force = desired_force

    def __call__(self, force):
        """
        Main call that takes in a measured force, filters it,
        runs the control loop, integrates and outputs the
        pwm(%) to send to motors
        """
        if force > 10.0:
            print 'Warning: Force value is too high'
            return self.pwm 
        self.filtered_force = self.force_filter.filterValue(force)
        self.error = (self.filtered_force - self.desired_force)
        # Max pwm change can be given in constructor of integral controller
        integral_out = self.integral_feedback_controller.control(self.error)
        pwm_out = integral_out
        
        if self.use_proportional_control:
            print self.proportional_feedback_controller.control(self.error)
            pwm_out += self.proportional_feedback_controller.control(self.error)
            
        self.pwm = np.clip(pwm_out, self.min_pwm, self.max_pwm)
        return self.pwm
        
        
