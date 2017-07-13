import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse
from multithreaded_getchar import MultiThreadedGetChar
from phidget_bridge import PhidgetBridge
from arduino_communication import ArduinoCommunication

# Add arg parser to read relevant options
parser = argparse.ArgumentParser(description='Collect steady state Force vs PWM data')
parser.add_argument('-p', '--port', type=str, help='Serial port', default='COM6')
parser.add_argument('-f', '--freq', type=float, help='Force sample frequency',
                    default=50)
parser.add_argument('-s', '--spin', type=float, help='Spin up delay for props',
                    default=3)
parser.add_argument('-t', '--timeon', type=float, help='Time to collect data',
                    default=5)
args = parser.parse_args()

# Main to calculate thrust vs. pwm, voltage vs. pwm, and thrust vs. time to
# determine a thrust curve for force control in quadcopters

frequency = args.freq  # (Hz)
spin_up_delay = args.spin  # delay time between motor PWM percentage change and collection of data
time_on = args.timeon  # (sec)
PWM_percentage_list = range(6, 25, 4)  # Starting, Ending, Interval times
avg_f_array = []  # Array for which the averaged forces are stored
std_f_array = []  # Array for which the standard deviations of the forces are stored
avg_v_array = []  # Array for which the averaged voltages are stored
std_v_array = []  # Array for which the standard deviations of the voltages are stored
p_array = []  # Array for whic the PWM's are stored
plt.ion()
plt.figure(1)
# Include phidgetbridge-related functions
phidget_bridge = PhidgetBridge(frequency)
# Include arduino-related functions
arduino_communication = ArduinoCommunication(port=args.port, baud_rate=115200)

# Checks to make sure the phidgetbridge is connected, and if not, exits program
try:
    phidget_bridge.waitingForConnection()
except:
    print "Phidget Bridge is not connected"
    exit(0)
if not phidget_bridge.connected_status:
    print "Phidget Bridge is not connected"
    exit(0)
continue_looping = True

# While no character is given, the loop will go through all PWM percentages and
# output forces and voltages per time
with MultiThreadedGetChar() as getchar:
    for i in range(0, len(PWM_percentage_list), 1):
        percentage = PWM_percentage_list[i]
        # Sends percentage to arduino to run the motor
        arduino_communication.sendMotorCommandToArduino(percentage)
        local_f_array = []  # local array to store force values
        local_v_array = []  # local array to store voltage values
        time.sleep(spin_up_delay)  # sleeps to ensure spin up time
        t_end = time.time() + time_on  # create end time variable from current time
        while time.time() < t_end:
            # Get force value from the load cell and add it to the local force
            # array
            local_f_array.append(phidget_bridge.getForce())
            # Get voltage value from the arduino and add it to the local
            # voltage array
            local_v_array.append(arduino_communication.getVoltageFromArduino())
            # If a characer is given, discontinue the loop and bring the motor
            # to 0 PWM
            if getchar():
                continue_looping = False
                arduino_communication.sendMotorCommandToArduino(0)
                break
            # sleep for a certain amount of time based on the given frequency
            time.sleep(1.0 / frequency)
        # If a character was given, discountinue the outerloop as well
        if not continue_looping:
            break
        # take current percentage and append to p_array
        p_array.append(percentage)
        # create an array from the local_f_array using numpy
        local_f_np_array = np.array(local_f_array)
        # create an array from the local_v_array using numpy
        local_v_np_array = np.array(local_v_array)
        # take the average of the local force array and store in the averaged
        # array
        avg_f_array.append(np.mean(local_f_np_array))
        # take the average of the local std force array and store in the
        # averaged array
        std_f_array.append(np.std(local_f_np_array))
        # take the average of the local voltage array and store in the averaged
        # array
        avg_v_array.append(np.mean(local_v_np_array))
        # take the average of the local std voltage array and store in the
        # averaged array
        std_v_array.append(np.std(local_v_np_array))
        # Creates two plots of all of the local force and voltage measurements
        plt.figure(1)
        plt.subplot(2, 1, 1)
        plt.plot(local_f_np_array)
        plt.subplot(2, 1, 2)
        plt.plot(local_v_np_array)
        plt.draw()
        # Prints to console the PWM, average force, and average voltage
        print "Current PWM: %f" % percentage
        print "Force - Mean: %f, Stdev: %f" % (avg_f_array[-1], std_f_array[-1])
        print "Voltage - Mean: %f, Stdev: %f" % (avg_v_array[-1], np.std(local_v_np_array))
        # Plots the average force vs. PWM
        plt.figure(2)
        plt.plot(p_array, avg_f_array, 'b*')
        plt.draw()
    # Turns the motor to 0 PWM
    arduino_communication.sendMotorCommandToArduino(0)

# If no percentage array is present, exit program
if not p_array:
    print "No data to plot"
    exit(0)

# PLots the thrust curve measurement vs. PWM percentages
plt.figure(3)
plt.errorbar(p_array, avg_f_array, yerr=std_f_array, fmt='ko-')
plt.title('Thrust Curve Measurement')
plt.xlabel('PWM percentage (%)')
plt.ylabel('Force (N)')

# Plots the battery voltage measurements vs. PWM percentages
plt.figure(4)
plt.errorbar(p_array, avg_v_array, yerr=std_v_array, fmt='ko-')
plt.title('Battery Voltage Measurement')
plt.xlabel('PWM percentage (%)')
plt.ylabel('Voltage (V)')

# Writes the PWM percentages, averaged forces, STD of the forces,
# averaged voltages, and STD of the voltages to a file
outfile = file('force_vs_pwm', mode='w+')
print>>outfile, p_array
print>>outfile, avg_f_array
print>>outfile, std_f_array
print>>outfile, avg_v_array
print>>outfile, std_v_array
outfile.close()

# Close the arduino and phidgetbridge connections
arduino_communication.closeArduino()
phidget_bridge.close()
print("Finished Calculating Measurements")
plt.show(block=True)
exit(0)
