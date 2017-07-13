from first_order_feedback_controller import FirstOrderFeedbackController
from online_low_pass_filter import OnlineButterLowPassFilter


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
        self.feedback_controller = FirstOrderFeedbackController()
        # For now not implemented adaptive gain estimator
        self.pwm = 6  # Start with minimal PWM percentage
        self.max_pwm_change = 0.05  # How much it can change in 1 cycle
        self.desired_force = 0
        self.filtered_force = 0
        self.dt = (1.0 / frequency)

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
        self.filtered_force = self.force_filter.filterValue(force)
        pwm_dot = self.feedback_controller.control(self.desired_force,
                                                   self.filtered_force)
        delta_pwm = min(pwm_dot * self.dt, self.max_pwm_change)
        self.pwm += delta_pwm
        return self.pwm
