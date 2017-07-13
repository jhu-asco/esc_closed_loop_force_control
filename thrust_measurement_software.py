import sys
import struct
import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from multithreaded_getchar import MultiThreadedGetChar


def VoltageRatioInputAttached(e):
    try:

        attached = e
        print("\nAttach Event Detected (Information Below)")
        print("===========================================")
        print("Library Version: %s" % attached.getLibraryVersion())
        print("Serial Number: %d" % attached.getDeviceSerialNumber())
        print("Channel: %d" % attached.getChannel())
        print("Channel Class: %s" % attached.getChannelClass())
        print("Channel Name: %s" % attached.getChannelName())
        print("Device ID: %d" % attached.getDeviceID())
        print("Device Version: %d" % attached.getDeviceVersion())
        print("Device Name: %s" % attached.getDeviceName())
        print("Device Class: %d" % attached.getDeviceClass())
        print("\n")

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)


def VoltageRatioInputDetached(e):
    detached = e
    try:
        print("\nDetach event on Port %d Channel %d" %
              (detached.getHubPort(), detached.getChannel()))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)


def ErrorEvent(e, eCode, description):
    print("Error %i : %s" % (eCode, description))


def VoltageRatioChangeHandler(e, voltageRatio):
    global forceSum
    global counter
    forceScaling = 4631.579
    force = forceScaling * voltageRatio * 9.81
    forceSum += force
    counter += 1


def SensorChangeHandler(e, sensorValue, sensorUnit):
    print("Sensor Value: %f" % sensorValue)

PWM_percentage_list = range(6, 81, 5)
port = 'com6'
baud_rate = 9600
voltage_scale = (5.0 / 1023.0) * 10.1
j = 0
total_battery = 0
forceSum = 0
counter = 0
f_array = []
p_array = []
v_array = []

arduino = serial.Serial(port, baud_rate)
time.sleep(2)

plt.ion()
plt.figure(1)
with MultiThreadedGetChar() as getchar:
    for i in range(0, len(PWM_percentage_list), 1):
        percentage = PWM_percentage_list[i]
        p_array.append(percentage)
        arduino.write(struct.pack('>B', percentage))
        time.sleep(2)
        while j < 10:
            data = arduino.read(2)
            if data:
                voltage = struct.unpack('<H', data)
                battery = voltage[0] * voltage_scale
                total_battery += battery
                j += 1
        try:
            ch = VoltageRatioInput()
        except RuntimeError as e:
            print("Runtime Exception %s" % e.details)
            print("Press Enter to Exit...\n")
            readin = sys.stdin.read(1)
            exit(1)
        try:
            ch.setOnAttachHandler(VoltageRatioInputAttached)
            ch.setOnDetachHandler(VoltageRatioInputDetached)
            ch.setOnErrorHandler(ErrorEvent)

            ch.setOnVoltageRatioChangeHandler(VoltageRatioChangeHandler)
            ch.setOnSensorChangeHandler(SensorChangeHandler)

            print("Waiting for the Phidget VoltageRatioInput Object to be attached...")
            ch.openWaitForAttachment(5000)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Press Enter to Exit...\n")
            readin = sys.stdin.read(1)
            exit(1)

        if(ch.getChannelSubclass() == ChannelSubclass.PHIDCHSUBCLASS_VOLTAGERATIOINPUT_BRIDGE):
            ch.setBridgeEnabled(1)

        print("Gathering data for 1 seconds...")
        time.sleep(1)

        AvgVoltage = total_battery / j
        AvgForce = forceSum / counter
        f_array.append(AvgForce)
        v_array.append(AvgVoltage)
        print("The average voltage (V) is: %f" % (AvgVoltage))
        print("The average force (N) is: %f" % (AvgForce))

        plt.plot(percentage, AvgForce, 'b*')

        try:
            ch.close()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Press Enter to Exit...\n")
            readin = sys.stdin.read(1)
            exit(1)
        plt.draw()
        if getchar():
            arduino.write(struct.pack('>B', 0))
            break
    arduino.write(struct.pack('>B', 0))

arduino.write(struct.pack('>B', 0))

plt.plot(p_array, f_array, 'ko-')
plt.title('Thrust Curve Measurement')
plt.xlabel('PWM percentage (%)')
plt.ylabel('Force (N)')

outfile = file('force_vs_pwm', mode='w+')
print>>outfile, p_array
print>>outfile, f_array
outfile.close()

arduino.close()
print("Finished Calculating Measurements")
plt.show(block=True)
exit(0)
