#ifndef MAIN_H
#define MAIN_H

#include <Arduino.h> //needed for Serial.println
#include <Encoder.h>
#include <MPU6050_tockn.h>
#include <NewPing.h>
#include <Servo.h>
#include <Wire.h>
#include <string.h> //needed for memcpy

/* Comms Configuration */
#define POLLING_FREQ 30

// Core operations
#define INIT_SENSORS 0x00
#define SELECT_IMU 0x01
#define SELECT_SONAR 0x02
#define SELECT_MOTOR 0x03
#define SELECT_ENCODER 0x04
#define SELECT_LINE_FOLLOWER 0x05

// IMU
#define ACCEL_X 0x10
#define ACCEL_Y 0x11
#define ACCEL_Z 0x12
#define GYRO_X 0x13
#define GYRO_Y 0x14
#define GYRO_Z 0x15
//TODO: Allow the changing of these
// #define SET_PIN_SDA     0x1A
// #define SET_PIN_SCL     0x1B
// #define SET_PIN_INT     0x1C

// Sonar
#define GET_DISTANCE_CM 0x20
#define SET_PIN_TRIGGER 0x2A
#define SET_PIN_ECHO 0x2B

// Motor controller
#define SET_PWM 0x30
#define GET_PWM 0x31
#define SET_PIN_PWM 0x3A

// Encoder
#define GET_ROTATION 0x40
#define SET_PIN_CH1 0x4A
#define SET_PIN_CH2 0x4B

// Line follower
#define GET_VALUE 0x50
#define SET_PIN_VAL 0x5A

/* ROBOT CONFIGURATION */

// IMU
#define NUM_IMUS 1
MPU6050 mpu6050(Wire);
MPU6050 imus[1] = { mpu6050 };

// Sonar Pins
#define NUM_SONARS 1
int max_distance = 150; // cm
NewPing* sonar;
uint8_t trig_pins[1] = { 9 };
uint8_t echo_pins[1] = { 8 };
NewPing* sonars[1] = { sonar };

// Motors
#define NUM_MOTORS 2
#define MAX_PWM 180
Servo leftMotor;
Servo rightMotor;
uint8_t motor_pins[2] = { 6, 5 };
uint8_t pwms[2] = { 90, 90 };
Servo motors[2] = { leftMotor, rightMotor };

// Encoder
#define NUM_ENCODERS 2
Encoder* leftEncoder;
Encoder* rightEncoder;
uint8_t ch1_pins[2] = { 13, 11 };
uint8_t ch2_pins[2] = { 12, 10 };
Encoder* encoders[2] = { leftEncoder, rightEncoder };

// Line followers
#define NUM_LINEFOLLOWERS 2

// A binary representation of a float to send on serial
typedef union {
    float floatingPoint;
    byte binary[4];
} binaryFloat;

// Selected components
uint8_t s_imu = 0;
uint8_t s_sonar = 0;
uint8_t s_motor = 0;
uint8_t s_encoder = 0;
uint8_t s_linefollower = 0;

#endif
