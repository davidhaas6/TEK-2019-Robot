#include <Servo.h>

Servo leftMotor;  // create servo object to control a servo
Servo rightMotor;

#define leftPin 6
#define rightPin 5

void setup() {
  Serial.begin(9600);
  leftMotor.attach(leftPin);
  rightMotor.attach(rightPin);

  Serial.println("** TESTING LEFT MOTOR **");
  leftMotor.write(20);
    rightMotor.write(20);

  delay(100000);
//  leftMotor.write(110);
//  delay(1000);
//  leftMotor.write(0);
//
//  Serial.println("** TESTING RIGHT MOTOR **");
//  rightMotor.write(70);
//  delay(1000);
//  rightMotor.write(110);
//  delay(1000);
//  rightMotor.write(0);
}

void loop() {
  // 0 - 89 is reverse w/ 0 being most powerful
  // 91 - 180 is forward w/ 180 being most powerful
  
}
