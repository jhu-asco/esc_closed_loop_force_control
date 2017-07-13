
int motorPin = 8; //motor connected to pin 8 on Arduino
int currentPin = A12; //current sensor connected to pin 12 on Arduino
int voltagePin = A13; //voltage sensor connected to pin 13 on Arduino
long baud_rate = 115200;
int speed; // indicates the duty cycle value (between 0 and 255)
int percentage; // indicates the percent of the duty cycle desired (should be between 0 and 30%)
double current; // current value
int MOTOR_ID = 1;
int VOLTAGE_ID = 2;
int minPWM = 128;
int maxPWM = 250;
double PWMscaling = (double)(maxPWM - minPWM) / 100.0;
double currentScaling = (5.0 / 1023.0)*17.0;
double voltageScaling = (5.0 / 1023.0)*10.1;


void setup() {
  pinMode(motorPin, OUTPUT);
  pinMode(voltagePin, INPUT);
  Serial.begin(baud_rate);
  percentage = 0;
  speed = PWMscaling * percentage + minPWM;
  analogWrite(motorPin, speed);
}

void data_repeat() {
  if (Serial.available() >= 2) {
    byte header = Serial.read();
    byte data = Serial.read();
    if (header == MOTOR_ID) {
        percentage = data;
        speed = PWMscaling * percentage + minPWM;
        analogWrite(motorPin, speed);
    }
    else if (header == VOLTAGE_ID){
      int voltage = analogRead(voltagePin);
      Serial.write((byte*)&voltage, 2);
    }
  }
}

void loop() {;
  data_repeat();
}
