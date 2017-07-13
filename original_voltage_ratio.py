# VoltageRatio from www.Phidgets.com
# (URL): https://www.phidgets.com/?tier=3&catid=2&pcid=1&prodid=35#product_tab_4
# under Resources and Code Samples

# This example reads and prints voltage values from the Phidgetbridge 
#connected to a load cell.

import sys
import struct
import time 
import serial
import matplotlib.pyplot as plt
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

try:
    ch = VoltageRatioInput()
except RuntimeError as e:
    print("Runtime Exception %s" % e.details)
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

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
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)

def ErrorEvent(e, eCode, description):
    print("Error %i : %s" % (eCode, description))

def VoltageRatioChangeHandler(e, voltageRatio):  
    print("Voltage Value: %f" % voltageRatio)

def SensorChangeHandler(e, sensorValue, sensorUnit):
    print("Sensor Value: %f" % sensorValue)

try:
    ch.setOnAttachHandler(VoltageRatioInputAttached)
    ch.setOnDetachHandler(VoltageRatioInputDetached)
    ch.setOnErrorHandler(ErrorEvent)

    ch.setOnVoltageRatioChangeHandler(VoltageRatioChangeHandler)
    ch.setOnSensorChangeHandler(SensorChangeHandler)

    # Please review the Phidget22 channel matching documentation for details on the device
    # and class architecture of Phidget22, and how channels are matched to device features.

    # Specifies the serial number of the device to attach to.
    # For VINT devices, this is the hub serial number.
    #
    # The default is any device.
    #
    # ch.setDeviceSerialNumber(<YOUR DEVICE SERIAL NUMBER>) 

    # For VINT devices, this specifies the port the VINT device must be plugged into.
    #
    # The default is any port.
    #
    # ch.setHubPort(0)

    # Specifies that the channel should only match a VINT hub port.
    # The only valid channel id is 0.
    #
    # The default is 0 (false), meaning VINT hub ports will never match
    #
    # ch.setIsHubPortDevice(1)

    # Specifies which channel to attach to.  It is important that the channel of
    # the device is the same class as the channel that is being opened.
    #
    # The default is any channel.
    #
    # ch.setChannel(0)

    # In order to attach to a network Phidget, the program must connect to a Phidget22 Network Server.
    # In a normal environment this can be done automatically by enabling server discovery, which
    # will cause the client to discovery and connect to available servers.
    #
    # To force the channel to only match a network Phidget, set remote to 1.
    #
    # Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICE);
    # ch.setIsRemote(1)

    print("Waiting for the Phidget VoltageRatioInput Object to be attached...")
    ch.openWaitForAttachment(5000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

if(ch.getChannelSubclass() == ChannelSubclass.PHIDCHSUBCLASS_VOLTAGERATIOINPUT_BRIDGE):
    ch.setBridgeEnabled(1)

print("Gathering data for 5 seconds...")
time.sleep(5)

try:
    ch.close()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1) 
print("Closed VoltageRatioInput device")
exit(0)
                     