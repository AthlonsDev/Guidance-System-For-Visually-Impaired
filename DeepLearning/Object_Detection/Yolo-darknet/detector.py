import cv2
import numpy as np

print(cv2.__version__)

# get the yolov4 weights and config file from darknet
net = cv2.dnn.readNet("/home/athlons/Documents/Final_Project/DeepLearning/Object_Detection/Yolo-darknet/darknet/yolov4.weights", "/home/athlons/Documents/Final_Project/DeepLearning/Object_Detection/Yolo-darknet/darknet/cfg/yolov4.cfg")
classes = []
with open("/home/athlons/Documents/Final_Project/DeepLearning/Object_Detection/Yolo-darknet/darknet/data/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading image
img = cv2.imread("room_ser.jpg")
img = cv2.resize(img, None, fx=0.4, fy=0.4)
height, width, channels = img.shape

# Detecting objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416,416), (0,0,0), True, crop=False)
net.setInput(blob)
outs = net.forward(output_layers)

# Showing informations on the screen
class_ids = []
confidences = []
boxes = []

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

indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4) #Remove overlapping bounding boxes
print(indexes)
font = cv2.FONT_HERSHEY_SIMPLEX

for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i] #Coordinates of the bounding box
        label = str(classes[class_ids[i]]) #Label of the object
        color = colors[i] #Color of the bounding box
        cv2.rectangle(img, (x,y), (x+w, y+h), color, 2) #Draw the bounding box
        cv2.putText(img, label, (x, y+30), font, 1, color, 2) #Write the label of the object

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()