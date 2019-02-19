

#include <Encoder.h>
#include <MPU6050_tockn.h>
#include <NewPing.h>
#include <Servo.h>
#include <Wire.h>

// Encoder
Encoder leftEncoder(13, 12);
Encoder rightEncoder(11, 10);

// IMU
MPU6050 mpu6050(Wire);

// MOTORS
Servo leftMotor; // create servo object to control a servo
Servo rightMotor;
#define leftPin 6
#define rightPin 5

// SONAR
#define TRIGGER_PIN 9 // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN 8 // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 150 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

void setup()
{
    Serial.begin(9600);
    Wire.begin();

    leftMotor.attach(6);
    rightMotor.attach(5);

    mpu6050.begin();
    mpu6050.calcGyroOffsets(true);

    Serial.println("Basic System Test\n");
}

float timer = 0;
void loop()
{
    mpu6050.update();

    if (millis() - timer > 3000) {
        Serial.println("\n\n\n*** MOTORS ***");
        Serial.println("Spinning left...");
        leftMotor.write(70);
        delay(500);
        leftMotor.write(110);
        delay(500);
        leftMotor.write(0);
        Serial.println("Spinning right...");
        rightMotor.write(70);
        delay(500);
        rightMotor.write(110);
        delay(500);
        rightMotor.write(0);

        Serial.println("*** IMU ***");
        Serial.print("accX : ");
        Serial.print(mpu6050.getAccX());
        Serial.print("\taccY : ");
        Serial.print(mpu6050.getAccY());
        Serial.print("\taccZ : ");
        Serial.println(mpu6050.getAccZ());
        Serial.print("gyroX : ");
        Serial.print(mpu6050.getGyroX());
        Serial.print("\tgyroY : ");
        Serial.print(mpu6050.getGyroY());
        Serial.print("\tgyroZ : ");
        Serial.println(mpu6050.getGyroZ());
        Serial.print("angleX : ");
        Serial.print(mpu6050.getAngleX());
        Serial.print("\tangleY : ");
        Serial.print(mpu6050.getAngleY());
        Serial.print("\tangleZ : ");
        Serial.println(mpu6050.getAngleZ());

        Serial.println("*** ENCODERS ***");
        Serial.print("Left: ");
        Serial.print(leftEncoder.read());
        Serial.print(" Right: ");
        Serial.println(rightEncoder.read());

        Serial.println("*** SONAR ***");
        for (int i = 0; i < 3; i++) {
            Serial.print("Ping: ");
            Serial.print(sonar.ping_cm()); // Send ping, get distance in cm and print result (0 = outside set distance range)
            Serial.println("cm");
            delay(50); // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.
        }
        timer = millis();
    }
}

