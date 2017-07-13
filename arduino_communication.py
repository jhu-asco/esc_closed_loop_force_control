import serial
import time
import struct

# Wrapper class to send PWM percentages and recieve battery voltages
# through Arduino


class ArduinoCommunication:

    # Create Constructor
    # Timeout: time for arduino to communicate with computer
    def __init__(self, port='com6', baud_rate=9600, timeout=2):
        # Scaling data value from analog input (1023) to voltage (5 V) with
        # voltage sensor scaling (10.1)
        self.voltage_scale = (5.0 / 1023.0) * 10.1
        self.MOTOR_ID = 1
        self.VOLTAGE_ID = 2
        # Connects with arduino
        self.arduino = serial.Serial(port, baud_rate)
        time.sleep(timeout)

    # Sends PWM percentages to the Arduino
    def sendMotorCommandToArduino(self, percentage=0):
        # Packs the data as big-endian integers and writes to the arduino
        # Motor header is the int 1, and percentage is sent as the PWM value
        self.arduino.write(struct.pack('>BB', self.MOTOR_ID, percentage))

    # Gets converted battery voltage values from the Arduino
    def getVoltageFromArduino(self):
        # Packs the data as big-endian integers and writes to arduino
        # Voltage header is the int 2, and the second byte refers to
        # unnecessary data
        self.arduino.write(struct.pack('>BB', self.VOLTAGE_ID, 0))
        # Reads and stores data from the arduino
        self.data = self.arduino.read(2)
        # if the data is not gibberish
        if self.data:
            # unpacks the data from the arduino as a little-endian integer and
            # stores into variable
            adc_output = struct.unpack('<H', self.data)
            # Converts data value to actual voltage
            voltage = adc_output[0] * self.voltage_scale
            return voltage
        return None

    # Closes the arduino connection
    def closeArduino(self):
        self.arduino.close()
