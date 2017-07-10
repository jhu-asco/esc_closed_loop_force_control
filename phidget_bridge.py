from Phidget22.Devices.VoltageRatioInput import VoltageRatioInput
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Phidget import ChannelSubclass

class PhidgetBridge:

    # Create constructor  
    def __init__(self, frequency = 20.0):
        self.connected_status = False
        self.force_scaling = 4631.579
        self.gravity = 9.81
        self.__force__ = 0
        self.time_interval = int(1000.0/frequency)
        self.createVoltageRatioInput()
    
    # Function to call handlers    
    def createVoltageRatioInput(self):
        self.ch = VoltageRatioInput()
        self.ch.setOnAttachHandler(self.voltageRatioInputAttached)
        self.ch.setOnDetachHandler(self.voltageRatioInputDetached)
        self.ch.setOnErrorHandler(self.errorEvent)
        self.ch.setOnVoltageRatioChangeHandler(self.voltageRatioChangeHandler)
    
    # Function to wait for a connection to the PhidgetBridge    
    def waitingForConnection(self, timeout=5000): 
        print("Waiting for the Phidget VoltageRatioInput Object to be attached...")
        self.ch.openWaitForAttachment(timeout)
        
    # Function for when the PhidgetBridge is attached
    # Prints status/information on connection & begins sending data
    def voltageRatioInputAttached(self, e):
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
            self.connected_status = True
            # Begins sending the data at the interval specified by frequency            
            if(self.ch.getChannelSubclass() == 
                ChannelSubclass.PHIDCHSUBCLASS_VOLTAGERATIOINPUT_BRIDGE):
                    self.ch.setBridgeEnabled(1)
                    if self.time_interval < self.ch.getMinDataInterval():
                        print "Time interval is too low: %i" % self.time_interval
                        self.time_interval = self.ch.getMinDataInterval()
                    elif self.time_interval > self.ch.getMaxDataInterval():
                        print "Time interval is too high: %i" % self.time_interval
                        self.time_interval = self.ch.getMaxDataInterval()
                    self.ch.setDataInterval(self.time_interval)
                    self.ch.setVoltageRatioChangeTrigger(0.0)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Press Enter to Exit...\n")
            self.connected_status = False
               
    # Function for detaching PhidgetBridge
    def voltageRatioInputDetached(self, e):
        detached = e
        self.connected_status = False
        try:
            print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Press Enter to Exit...\n")
            
    # Function for errors 
    def errorEvent(self, e, eCode, description):
        print("Error %i : %s" % (eCode, description))
    
    # Handler to calculate force from voltageRatio
    def voltageRatioChangeHandler(self, e, voltageRatio):  
        self.__force__ = self.force_scaling*voltageRatio*self.gravity
   
    # Gets force from voltageRatioChangeHandler
    def getForce(self):
        return self.__force__
    
    # Closes PhidgetBridge
    def close(self):
        self.ch.close()
        
        
