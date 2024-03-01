import serial
import serial.serialutil as serialutil
from queue import Queue
import threading as th
import time

# Configure the serial connection
port = "dev/ttyACM0"
#speed of data transfer in bits per second
bitrate = 115200
# Open the serial connection, with a set bitrate, and a timeout set to 1.5 seconds, so that the connection is closed if no data is received for 1.5 seconds
serial_connection = serial.Serial('/dev/ttyACM0', bitrate, timeout=5.5) # Open

if not serial_connection.is_open: # Check if the serial connection is open
    serial_connection.open() # Open the serial connection

q = Queue()
def get_distance():
    if serial_connection.is_open: # Check if the serial connection is open
        try:
            data = serial_connection.read(128)  # Read the data from the serial connection up to 128 bytes

            while True:
                if data == b"EOF": # b is for byte string and EOF is the end of file
                    break
            # wait 1 second before reading again
                # time.sleep(0.001)
            #convert bytes to string an strip \n and \r
                newdata = data.split(b'\r')[0]
                intData = int(newdata)
                print(intData)
                # q.put(intData)
        except serialutil.SerialException:
            print("couldn read from device") # Print an error message if the data could not be read from the serial connection
    
    else:
        print("Serial port is not open.")
        #open the connection
        

serial = serial.Serial('/dev/ttyACM0', 9600)
def read_data():
    try:
        data = serial.readline()
        if data == b"EOF":
            return -1
        newdata = data.split(b'\r')[0]
        #remove b' and ' from the string
        newdata = str(newdata)[2:-1]
        intData = int(newdata)
        # print(intData)
        if not intData == None:
            q.put(intData)
        return intData
    except serialutil.SerialException:
        # print("couldn read from device")
        return -1

# Close the files and serial connection
serial_connection.close()