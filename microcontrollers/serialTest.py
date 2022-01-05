# NOTE: to be paired with the arduino code test.ino in the microcontrollers folder

# import serial
import serial
import time

# be careful with the port - it depends on what computer you're on, this is what returned for my mac but check using your Arduino compiler and change accordingly
arduino = serial.Serial(port='/dev/cu.usbmodem2401', baudrate=115200, timeout=.1)

# test function - returns the underlying data, need to convert to ascii if you want it to be readable
# the function should take an input and then return it +1
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
while True:
    num = input("Enter a number: ") # Taking input from user
    value = write_read(num)
    print(value) # printing the value