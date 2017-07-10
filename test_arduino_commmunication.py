from arduino_communication import ArduinoCommunication
import numpy as np
import time

percentage_array = np.linspace(6,55, 5)
arduino_communication = ArduinoCommunication()
for i in range(0, len(percentage_array), 1):
    percent = percentage_array[i]
    arduino_communication.sendMotorCommandtoArduino(percent)
    time.sleep(2)
    print(arduino_communication.getVoltageFromArduino())
arduino_communication.sendMotorCommandtoArduino(0)
arduino_communication.closeArduino()