# Proportional Feedback 

class ProportionalFeedbackController:
    
    # Constructor 
    # Parameters: proportional_pwm_gain
    # User defined variable to set proportional gain constant
    def __init__ (self, proportional_pwm_gain = 1):
        # Check to make sure that the gain is greater than zero
        assert(proportional_pwm_gain > 0)
        # Set as a variable within class to call/use
        self.proportional_pwm_gain = proportional_pwm_gain
    
    # Proportional Control 
    # Parameters: error
    # Variable passed in from control loop indicating error between given
    # force value and desired force vale    
    def control(self, error):
        # Returns proportional portion of control 
        return -(self.proportional_pwm_gain) * (error)