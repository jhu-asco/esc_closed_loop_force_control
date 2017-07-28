# Proportional Feedback 

class ProportionalFeedbackController:
    
    # Constructor 
    def __init__ (self, proportional_pwm_gain = 1):
        assert(proportional_pwm_gain > 0)
        self.proportional_pwm_gain = proportional_pwm_gain
        
    def control(self, error):
        return -(self.proportional_pwm_gain) * (error)