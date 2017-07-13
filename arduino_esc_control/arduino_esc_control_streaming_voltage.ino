#include <SimpleTimer.h>

int motorPin = 8; //motor connected to pin 8 on Arduino
int currentPin = A12; //current sensor connected to pin 12 on Arduino
int voltagePin = A13; //voltage sensor connected to pin 13 on Arduino
int speed; // indicates the duty cycle value (between 0 and 255)
int percentage; // indicates the percent of the duty cycle desired (should be between 0 and 30%)
double current; // current value
//double voltage; // volage value
int minPWM = 128;
int maxPWM = 250;
double PWMscaling = (double)(maxPWM - minPWM) / 100.0;
double currentScaling = (5.0 / 1023.0)*17.0;
double voltageScaling = (5.0 / 1023.0)*10.1;

SimpleTimer serial_timer;
SimpleTimer sensor_timer;

void setup() {
  pinMode(motorPin, OUTPUT);
  //pinMode(currentPin, INPUT);
  pinMode(voltagePin, INPUT);
  Serial.begin(9600);
  //Serial.println("Enter a duty cycle percentage: ");
  percentage = 0;
  speed = PWMscaling * percentage + minPWM;
  analogWrite(motorPin, speed);
  serial_timer.setInterval(10, motor_repeat);
  sensor_timer.setInterval(100, vc_repeat);
}

void motor_repeat() {
  if (Serial.available()) {
    percentage = Serial.read();
    speed = PWMscaling * percentage + minPWM;
    //Serial.println(percentage);
    if (percentage >= 0 && percentage <= 100) {
      //Serial.println(speed);
     analogWrite(motorPin, speed);
    }
    else {
      //Serial.print("Warning: the value is: ");
      //Serial.print(speed);
      //Serial.println("! This is above the value threshold!");
    }
    //Serial.println("Enter a duty cycle percentage: ");
  }
}

void vc_repeat() {
  /*int currentPinReading = analogRead(currentPin);
  if(currentPinReading != 0) {
    //current = (currentPinReading) * currentScaling;
    Serial.print("Current is: ");
    Serial.println(currentPinReading);
  }
  Serial.println(" (?)"); */
  //voltage = (analogRead(voltagePin)) * voltageScaling;
  int voltage = analogRead(voltagePin);
  //Serial.print("Voltage is: ");
  Serial.write((byte*)&voltage, 2);
  //Serial.println(" (V)"); 
}

void loop() {
  serial_timer.run();
  sensor_timer.run();
}
