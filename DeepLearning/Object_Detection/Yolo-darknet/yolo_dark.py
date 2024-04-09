import cv2
import numpy as np
import time
import threading as th
import Speech as sp
import Receiver as rc
# import img2text as it

print(cv2.__version__)

CONFIDENCE_THRESHOLD = 0.6 #Confidence treshold, lowering it will aloow more objects detected but at lower accuracy
NMS_THRESHOLD = 0.5 #Non-maximum suppression threshold, lowering it will allow more boxes to be drawn, but at lower accuracy
COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)] #Colors for the boxes



def get_classnames(labels_path):
    class_names = []
    with open(labels_path, "r") as f:
        class_names = [cname.strip() for cname in f.readlines()]
    return class_names

def setup_camera(video_input):
    vc = cv2.VideoCapture(0) 
    return vc

def load_model(weight_path, config_path):
    net = cv2.dnn.readNetFromDarknet(config_path, weight_path)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    return net


def pre_processing(net) :
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(125, 125), scale=1/255, swapRB=True)
    return model


def say(text):
    print(text)
    t = th.Thread(target=sp.speak, args=(text,))
    t.start()

distance = 0
def read_distance():
    q = rc.q
    # t = th.Thread(target=lambda q, arg: (rc.read_data()), args=(q, 2))
    t = th.Thread(target=rc.read_data) # call read_data function from Receiver.py in a new thread
    t.start() # start the thread
    # print(q.get())
    while not q.empty(): # check if the queue is not empty
        # print(q.get()) # print the value in the queue0
        return q.get() # return the value in the queue

def take_pic(vc):
    value, frame = vc.read()
    cv2.imwrite(f"DeepLearning/Object_Detection/Yolo-darknet/pic.jpg", frame)
    run_img_to_text(f"DeepLearning/Object_Detection/Yolo-darknet/pic.jpg")

def run_img_to_text(pic_path):
    it.img_to_text(pic_path)


def detect_objects(vc, model, class_names):
    # camer keeps running until user presses 'q'
    while cv2.waitKey(1) < 1:
        (grabbed, frame) = vc.read()
        if not grabbed:
            exit()

        if cv2.waitKey(1) == ord('c'):
            take_pic(vc)
            print("Picture taken")
            continue
            # say("Picture taken

        # print("Frame shape: ", frame.shape)
        current_obj = ""
        classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)

        # read_distance()
        distance = read_distance()

        try:
            if len(classes) != 0:
                for (classid, score, box) in zip(classes, scores, boxes):
                    color = COLORS[int(classid) % len(COLORS)]
                    class_index = int(classid)
                    label = "%s : %f" % (class_names[class_index], score)
                    cv2.rectangle(frame, box, color, 2)
                    cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    current_obj = class_names[class_index]
                    box_pos = (box[0] + box[2]) // 2 # get the x position of the box by adding the x and width and dividing by 2
                    # print(box_pos)
                    if box_pos <= 200.66:
                        position = "left"
                    elif box_pos >= 300.33:
                        position = "right"
                    elif box_pos <= 300.33 and box_pos >= 200.66:
                        position = "middle"
                # print(f"{current_obj} is {distance}centimeters away and is on the {position}")
                if not distance == None and distance < 100:
                    print(f"{current_obj} is on the {position} at {distance}cm")
                    # say(f"{current_obj} is on the {position} at {distance} centimeters")
                    pass
        except TypeError:
            print("No object detected")\
            
        # fps_label = "FPS: %.2f " % (1 / (end - start), (end_drawing - start_drawing) * 1000)
        # cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow("detections", frame)

if __name__ == "__main__":
    weight_path = "DeepLearning/Object_Detection/Yolo-darknet/yolov7-tiny.weights"
    config_path = "DeepLearning/Object_Detection/Yolo-darknet/yolov7-tiny.cfg"
    labels_path = "DeepLearning/Object_Detection/Yolo-darknet/coco-classes.txt"
    video_input = 0

    class_names = get_classnames(labels_path)
    net = load_model(weight_path, config_path)
    model = pre_processing(net)
    video = setup_camera(video_input)
    detect_objects(video, model, class_names)


