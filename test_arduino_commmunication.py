#Test for the Ardufly/pilot/Mega: Sending PWM signals and recieving battery voltage values
# Written by: Joseph Chung under ASCOL
# Email: jchung55@jhu.edu
# Date: 7/11/17

from arduino_communication import ArduinoCommunication
import numpy as np
import time

# Create a percentage array of motor values
percentage_array = np.linspace(6, 55, 5)
# Instantiate the class into main
arduino_communication = ArduinoCommunication()
# Send motor commands to the arduino and recieve voltage values 
for i in range(0, len(percentage_array), 1):
    percent = percentage_array[i]
    arduino_communication.sendMotorCommandToArduino(percent)
    time.sleep(2)
    print(arduino_communication.getVoltageFromArduino())
# Reset the motor to zero (0) after all trials are done
arduino_communication.sendMotorCommandToArduino(0)
# Close the arduino
arduino_communication.closeArduino()