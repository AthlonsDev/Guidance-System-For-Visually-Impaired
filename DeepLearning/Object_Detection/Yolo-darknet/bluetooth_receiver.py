from queue import Queue
import threading as th
import time

q = Queue()
#get data from bluetooth connected device
device = "/dev/rfcomm0"

def read_data():
    with open(device, "r") as f:
        while True:
            data = f.read()
            if data == "EOF":
                break
            time.sleep(1)
            newdata = data.split("\r")[0]
            try:
                intData = int(newdata)
            except ValueError:
                print("Invalid data received")
                return 0
            q.put(intData)
            print(intData)