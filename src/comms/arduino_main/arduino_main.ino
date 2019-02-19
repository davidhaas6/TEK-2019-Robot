#include "main.h"

void setup()
{
    Serial.begin(9600); // Open serial monitor at 9600 baud to see ping results.
    Wire.begin();
}

void init_sensors()
{
    // Init IMU
    for (int i = 0; i < NUM_IMUS; i++) {
        imus[i].begin();
        imus[i].calcGyroOffsets(true);
    }

    // Attach motors to drivers
    for (int i = 0; i < NUM_MOTORS; i++) {
        motors[i].attach(motor_pins[i]);
    }

    // Init sonar with new pins
    for (int i = 0; i < NUM_SONARS; i++) {
        sonars[i] = new NewPing(trig_pins[i], echo_pins[i], max_distance);
    }

    // Init encoders
    for (int i = 0; i < NUM_ENCODERS; i++) {
        encoders[i] = new Encoder(ch1_pins[i], ch2_pins[i]);
    }
}

byte inByte;
void loop()
{
    delay(1000 / POLLING_FREQ);

    // Update IMUs
    for (int i = 0; i < NUM_IMUS; i++) {
        imus[i].update();
    }

    if (Serial.available() > 0) {
        // get incoming byte:
        process_command(Serial.read());
    }
}

void wait_for_input()
{
    while (Serial.available() <= 0) {
        delay(1000 / POLLING_FREQ);
        for (int i = 0; i < NUM_IMUS; i++) {
            imus[i].update();
        }
    }
}

bool fill_variable(uint8_t& var, const uint8_t& max_value)
{
    wait_for_input();
    uint8_t buff = Serial.read();
    if (buff < max_value) {
        var = Serial.read();
        return true;
    }
    return false;
}

void write_float(const float& val)
{
    binaryFloat data;
    data.floatingPoint = val;
    Serial.write(data.binary, 4);
}

void process_command(byte cmd)
{
    switch (cmd) {
    // Core Arduino
    case INIT_SENSORS:
        init_sensors();
        break;
    case SELECT_IMU:
        fill_variable(s_imu, NUM_IMUS);
        break;
    case SELECT_SONAR:
        fill_variable(s_sonar, NUM_SONARS);
        break;
    case SELECT_MOTOR:
        fill_variable(s_motor, NUM_MOTORS);
        break;
    case SELECT_ENCODER:
        fill_variable(s_encoder, NUM_ENCODERS);
        break;
    case SELECT_LINE_FOLLOWER:
        fill_variable(s_linefollower, NUM_LINEFOLLOWERS);
        break;

    // IMU
    case ACCEL_X:
        write_float(imus[s_imu].getAccX());
        break;
    case ACCEL_Y:
        write_float(imus[s_imu].getAccY());
        break;
    case ACCEL_Z:
        write_float(imus[s_imu].getAccZ());
        break;
    case GYRO_X:
        write_float(imus[s_imu].getGyroX());
        break;
    case GYRO_Y:
        write_float(imus[s_imu].getGyroY());
        break;
    case GYRO_Z:
        write_float(imus[s_imu].getGyroZ());
        break;

    // Sonar
    case GET_DISTANCE_CM:
        write_float(sonars[s_sonar]->ping_cm());
        break;
    case SET_PIN_TRIGGER:
        if (fill_variable(trig_pins[s_sonar], NUM_SONARS)) {
            delete sonars[s_sonar];
            sonars[s_sonar] = new NewPing(trig_pins[s_sonar], echo_pins[s_sonar], max_distance);
        }
        break;
    case SET_PIN_ECHO:
        if (fill_variable(echo_pins[s_sonar], NUM_SONARS)) {
            delete sonars[s_sonar];
            sonars[s_sonar] = new NewPing(trig_pins[s_sonar], echo_pins[s_sonar], max_distance);
        }
        break;

    // Motor controller
    case SET_PWM:
        if (fill_variable(pwms[s_motor], MAX_PWM + 1)) {
            motors[s_motor].write(pwms[s_motor]);
        }
        break;
    case GET_PWM:
        Serial.write(pwms[s_motor]);
        break;
    case SET_PIN_PWM:
        if (fill_variable(motor_pins[s_motor], NUM_MOTORS)) {
            motors[s_motor].attach(motor_pins[s_motor]);
        }
        break;

    // Encoder
    case GET_ROTATION:
        write_float(encoders[s_encoder]->read());
        break;
    case SET_PIN_CH1:
        if (fill_variable(ch1_pins[s_encoder], NUM_ENCODERS)) {
            delete encoders[s_encoder];
            encoders[s_encoder] = new Encoder(ch1_pins[s_encoder], ch2_pins[s_encoder]);
        }
        break;
    case SET_PIN_CH2:
        if (fill_variable(ch2_pins[s_encoder], NUM_ENCODERS)) {
            delete encoders[s_encoder];
            encoders[s_encoder] = new Encoder(ch1_pins[s_encoder], ch2_pins[s_encoder]);
        }
        break;

    // Line follower
    case GET_VALUE:
        break;
    case SET_PIN_VAL:
        break;
    }
}
