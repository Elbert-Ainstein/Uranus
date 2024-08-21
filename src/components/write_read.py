import serial
import time

arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1) 


def write_read(x): 
    if not arduino.isOpen():
        arduino.open()
    # print('com3 is open', arduino.isOpen())
    print(x)
    arduino.write(x.encode())
    time.sleep(0.05) 
    data = arduino.readline() 
    return data 
