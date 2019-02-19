#line 1 "/Users/david/Documents/TEK/programming_robot/src/main.h"
#line 1 "/Users/david/Documents/TEK/programming_robot/src/main.h"
#ifndef MAIN_H
#define MAIN_H

#include <Arduino.h> //needed for Serial.println
#include <string.h> //needed for memcpy

// Core operations
#define INIT_SENSORS    0x00
#define SELECT_IMU	    0x01
#define SELECT_SONAR	0x02
#define SELECT_MOTOR	0x03
#define SELECT_ENCODER	0x04
#define SELECT_LINE_FOLLOWER 0x05

// IMU
#define ACCEL_X	        0x10
#define ACCEL_Y	        0x11
#define ACCEL_Z	        0x12
#define GYRO_X	        0x13
#define GYRO_Y	        0x14
#define GYRO_Z	        0x15

// Sonar
#define GET_DISTANCE_CM	0x20

// Motor controller
#define SET_PWM	        0x30
#define GET_PWM	        0x31

// Encoder
#define GET_ROTATION	0x40

// Line follower
#define GET_VALUE	    0x50

#endif
#line 1 "/Users/david/Documents/TEK/programming_robot/src/main.ino"
#include <Servo.h>
#include <Encoder.h>
#include <MPU6050_tockn.h>
#include <NewPing.h>
#include "main.h"


// Sonar Pins
#define TRIGGER_PIN 9
#define ECHO_PIN 8
#define MAX_DISTANCE 150 // cm
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

void setup()
{
    Serial.begin(9600); // Open serial monitor at 9600 baud to see ping results.
    while(Serial.available <= 0) {delay(10);}
}

// void loop()
// {
//     if (Serial.available() > 0)
//     {
//         // get incoming byte:
//         inByte = Serial.read();
//         delay(50); // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.
//         Serial.print("Ping: ");
//         Serial.print(sonar.ping_cm()); // Send ping, get distance in cm and print result (0 = outside set distance range)
//         Serial.println("cm");
//     }
// }
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

