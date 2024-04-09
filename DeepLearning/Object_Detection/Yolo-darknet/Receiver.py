import serial
import serial.serialutil as serialutil
from queue import Queue
import threading as th
import time

# Configure the serial connection
port = "/dev/ttyACM0"
#speed of data transfer in bits per second
bitrate = 115200
# Open the serial connection, with a set bitrate, and a timeout set to 1.5 seconds, so that the connection is closed if no data is received for 1.5 seconds
serial_connection = serial.Serial(port, bitrate, timeout=1.5) # Open

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
                time.sleep(1)
                newdata = data.split(b'\r')[0]
                try:
                    intData = int(newdata)
                except ValueError:
                    print("Invalid data received")
                    return 0
                # q.put(intData)
                print(intData)
        except serialutil.SerialException:
            print("couldn read from device") # Print an error message if the data could not be read from the serial connection
            return 0
    else:
        print("Serial port is not open.")
        #open the connection
        serial_connection.open()


serial = serial.Serial('/dev/ttyACM0', 9600)
def read_data():
    try:
        data = serial.read_all()
        if data == b"EOF":
            return 0
        time.sleep(1)
        newdata = data.split(b'\r')[0]
        #remove b' and ' from the string
        newdata = str(newdata)[2:-1]
        try:
            intData = int(newdata)
            q.put(intData)
            return intData
        except ValueError:
            return 0
    except serialutil.SerialException:
        print("couldn read from device")
        return 0
    
if __name__ == "__main__":
    while True:
        print(read_data())
        # print(q.get())
        # print(get_distance

# Close the files and serial connection
serial_connection.close()