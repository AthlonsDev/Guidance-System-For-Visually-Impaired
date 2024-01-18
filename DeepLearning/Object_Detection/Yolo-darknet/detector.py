import cv2
import numpy as np


print(cv2.__version__)

# get the yolov4 weights and config file from darknet
net = cv2.dnn.readNet("/home/athlons/Documents/Final_Project/DeepLearning/Object_Detection/Yolo-darknet/darknet/yolov4.weights", "/home/athlons/Documents/Final_Project/DeepLearning/Object_Detection/Yolo-darknet/darknet/cfg/yolov4.cfg")

with open("/home/athlons/Documents/Final_Project/DeepLearning/Object_Detection/Yolo-darknet/darknet/data/coco.names", "r") as f:
    classes = f.read().splitlines()

print(classes)

#test model with image
img = cv2.imread("/home/athlons/Documents/Final_Project/DeepLearning/Object_Detection/Yolo-darknet/darknet/data/dog.jpg")
height, width, _ = img.shape

# get the names of the output layers
layer_names = net.getLayerNames()
print(layer_names)
for i in net.getUnconnectedOutLayers():
    print(layer_names[i[0]-1])

# convert image to blob
blob = cv2.dnn.blobFromImage(img, 0.00392, (416,416), (0,0,0), True, crop=False)

# set the input for the net
net.setInput(blob)

# get the output from the net
outs = net.forward(output_layers)

# get the confidence, class id, and bounding box coordinates
confidences = []
class_ids = []
boxes = []

# loop through each output layer and get the confidence, class id, and bounding box coordinates
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores) #Index of the class with the highest score
        confidence = scores[class_id] #Confidence of the class with the highest score
        if confidence > 0.5:
            # Object detected
            center_x = int(detection[0]*width) #Center x of the object
            center_y = int(detection[1]*height) #Center y of the object
            w = int(detection[2]*width) #Width of the object
            h = int(detection[3]*height) #Height of the object

            # Rectangle coordinates
            x = int(center_x - w/2) #Top left x
            y = int(center_y - h/2) #Top left y

            boxes.append([x, y, w, h])

            confidences.append(float(confidence))
            class_ids.append(class_id)