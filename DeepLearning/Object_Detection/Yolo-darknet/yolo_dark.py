import cv2
import time
import threading as th
import Speech as sp
# import Receiver as rc

print(cv2.__version__)

CONFIDENCE_THRESHOLD = 0.2
NMS_THRESHOLD = 0.4
COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]


class_names = []
with open("coco-classes.txt", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

# vc = cv2.VideoCapture("/home/athlons/Documents/Final_Project/realtime_obj_det/test_videos/video-2.mp4")
vc = cv2.VideoCapture(0)
focus = 255 #min: 0, max: 255, increment: 5
# prop = cv2.CAP_PROP_FOCUS
# vc.set(prop, focus)

net = cv2.dnn.readNet("yolov7-tiny.weights", "yolov7-tiny.cfg")
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
    # time.sleep(1)
    t = th.Thread(target=lambda q, arg: (rc.read_data()), args=(q, 2))
    # t = th.Thread(target=rc.read_data)
    t.daemon = True
    t.start()
    if not q.empty() and not q == None:
        # print(q.get())
        return(int(q.get()))
        # return distance
    

while cv2.waitKey(1) < 1:
    (grabbed, frame) = vc.read()
    if not grabbed:
        exit()

    current_obj = ""
    start = time.time()
    classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    end = time.time()
    start_drawing = time.time()

    # read_distance()
    # distance = read_distance()
    try:
        # if distance > 0 and distance < 100:
            if len(classes) != 0:
                classid, score, box = classes[0], scores[0], boxes[0]
                color = COLORS[int(classid) % len(COLORS)]
                class_index = int(classid)
                label = "%s : %f" % (class_names[class_index], score)
                cv2.rectangle(frame, box, color, 2)
                cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                current_obj = class_names[class_index]
            #th.Thread(target=say, args=(current_obj,)).start()
            print(current_obj + " " + str(distance) + "cm")
    except TypeError:
        print("No object detected")
    

    end_drawing = time.time()
    
    # fps_label = "FPS: %.2f " % (1 / (end - start), (end_drawing - start_drawing) * 1000)
    # cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.imshow("detections", frame)