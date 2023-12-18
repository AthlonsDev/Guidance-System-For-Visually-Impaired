import serial
import time

# Configure the serial connection
port = "COM6" 
#speed of data transfer in bits per second
bitrate = 115200
# Open the serial connection, with a set bitrate, and a timeout set to 1.5 seconds, so that the connection is closed if no data is received for 1.5 seconds
serial_connection = serial.Serial(port, bitrate, timeout=1.5)

# Open a file on your computer to write the received data
# destination_file = open("/Users/mahmoodshilleh/Desktop/store_info.txt", "wb")

# Read and write data until the transfer is complete
while True:
    # Read 128 bytes of data from the serial connection
    data = serial_connection.read(128)
    if data == b"EOF": # b is for byte string and EOF is the end of file
        break
    # wait 1 second before reading again
    time.sleep(1)
    # print(data)
    #convert bytes to string and remove \n and \r
    newdata = data.decode("utf-8").strip().replace("\n", "").replace("\r", "").split(" ")[0]
    # print(newdata)
    if newdata != "": # if data is not empty
        # convert string to int
        intdata = int(newdata) # convert string to int
        # intdata = int(fdata)
        print(intdata, "cm")
        # if intdata < 70:
        #     print("Object is close, activate model ")
        # else:
        #     print("Object is far, deactivate model")
        # print(intdata)
    # print(newdata)



# Close the files and serial connection
# destination_file.close()
serial_connection.close()

COM6 = serial.Serial('COM6', 9600)
while True:
    data = COM6.readline()
    print(data)