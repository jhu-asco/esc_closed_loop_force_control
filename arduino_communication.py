import serial
import time
import struct

class ArduinoCommunication:
    
    def __init__(self):
        self.voltage_scale = (5.0/1023.0)*10.1
        self.port = 'com6'
        self.baud_rate = 9600
        self.connectingWithArduino()
    
    def connectingWithArduino(self, timeout = 2):
        self.arduino = serial.Serial(self.port, self.baud_rate)
        time.sleep(timeout)
    
    def sendMotorCommandtoArduino(self, percentage = 0):
        self.arduino.write(struct.pack('>B', percentage))
        
    def getVoltageFromArduino(self):    
        self.data = self.arduino.read(2)
        if self.data:
            adc_output = struct.unpack('<H', self.data)
            voltage = adc_output[0]*self.voltage_scale
            return voltage
        return None
        
    def closeArduino(self):
        self.arduino.close()
    
    