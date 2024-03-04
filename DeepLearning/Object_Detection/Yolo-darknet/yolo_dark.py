import cv2
import time
import threading as th
import Speech as sp
# import Receiver as rc

print(cv2.__version__)

CONFIDENCE_THRESHOLD = 0.5 #Confidence treshold, lowering it will aloow more objects detected but at lower accuracy
NMS_THRESHOLD = 0.5 #Non-maximum suppression threshold, lowering it will allow more boxes to be drawn, but at lower accuracy
COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)] #Colors for the boxes


class_names = []
with open("DeepLearning/Object_Detection/Yolo-darknet/coco-classes.txt", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

# vc = cv2.VideoCapture("/home/athlons/Documents/Final_Project/realtime_obj_det/test_videos/video-2.mp4")
vc = cv2.VideoCapture(0)
focus = 255 #min: 0, max: 255, increment: 5
# prop = cv2.CAP_PROP_FOCUS
# vc.set(prop, focus)
net = cv2.dnn.readNetFromDarknet("DeepLearning/Object_Detection/Yolo-darknet/yolov7-tiny.cfg", "DeepLearning/Object_Detection/Yolo-darknet/yolov7-tiny.weights")
# net = cv2.dnn.readNet("DeepLearning/Object_Detection/Yolo-darknet/yolov7-tiny.weights", "DeepLearning/Object_Detection/Yolo-darknet/yolov7-tiny.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(125, 125), scale=1/255, swapRB=True)

def say(text):
    print(text)
    sp.speak(text)

distance = 0
def read_distance():
    q = rc.q
    # t = th.Thread(target=lambda q, arg: (rc.read_data()), args=(q, 2))
    t = th.Thread(target=rc.read_data) # call read_data function from Receiver.py in a new thread
    t.start() # start the thread
    # print(q.get())
    while not q.empty(): # check if the queue is not empty
        print(q.get()) # print the value in the queue0


while cv2.waitKey(1) < 1:
    (grabbed, frame) = vc.read()
    if not grabbed:
        exit()

    # print("Frame shape: ", frame.shape)
    current_obj = ""
    start = time.time()
    classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    end = time.time()
    start_drawing = time.time()

    # read_distance()
    # distance = read_distance()

    try:
        if len(classes) != 0:
            classid, score, box = classes[0], scores[0], boxes[0]
            color = COLORS[int(classid) % len(COLORS)]
            class_index = int(classid)
            label = "%s : %f" % (class_names[class_index], score)
            cv2.rectangle(frame, box, color, 2)
            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            current_obj = class_names[class_index]
        # if distance > 0 and distance < 100:
            # to get the position of the object, i will use the box variable
            #320 is the maximum horizontal size from left to right, so that is divided in three parts of
            box_pos = (box[0] + box[2]) // 2 # get the x position of the box by adding the x and width and dividing by 2
            # print(box_pos)
            if box_pos <= 183.66:
                position = "left"
            elif box_pos >= 300.33:
                position = "right"
            elif box_pos <= 300.33 and box_pos >= 183.66:
                position = "middle"
            # print(f"{current_obj} is {distance}centimeters away and is on the {position}")
            print(f"{current_obj} is on the {position}")
            # sp.speak(current_obj + " " + str(distance) + "cm")
            # th.Thread(target=say, args=(current_obj,)).start()
    except TypeError:
        print("No object detected")
    

    end_drawing = time.time()
    
    # fps_label = "FPS: %.2f " % (1 / (end - start), (end_drawing - start_drawing) * 1000)
    # cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.imshow("detections", frame)