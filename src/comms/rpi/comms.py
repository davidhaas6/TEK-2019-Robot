import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.flushInput()

usr_input = ""
usr_input = input("Enter the byte to send: ")
while usr_input != "x":
    byte = int(usr_input, 16)
    ser.write(bytes([byte]))

    time.sleep(.1)
    if ser.in_waiting:
        print(ser.read())

    usr_input = input("Enter the byte to send (enter 'x' to stop): ")
