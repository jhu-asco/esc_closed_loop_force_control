# Test for the Ardufly/pilot/Mega: Sending PWM signals and recieving battery voltage values
# Written by: Joseph Chung under ASCOL
# Email: jchung55@jhu.edu
# Date: 7/11/17

from arduino_communication import ArduinoCommunication
import numpy as np
import time
import argparse

# Get arguments from commandline
parser = argparse.ArgumentParser(description='Test arduino communication.')
parser.add_argument('-p', '--port', type=str, help='Serial port', default='COM6')
args = parser.parse_args()
# Create a percentage array of motor values
percentage_array = np.linspace(6, 6, 5)
# Instantiate the class into main
arduino_communication = ArduinoCommunication(port=args.port, baud_rate=115200)
# Send motor commands to the arduino and recieve voltage values
for i in range(0, len(percentage_array), 1):
    percent = percentage_array[i]
    print percent
    arduino_communication.sendMotorCommandToArduino(percent)
    time.sleep(2)
    print "done sleeping"
    print(arduino_communication.getVoltageFromArduino())
# Reset the motor to zero (0) after all trials are done
arduino_communication.sendMotorCommandToArduino(0)
# Close the arduino
arduino_communication.closeArduino()
