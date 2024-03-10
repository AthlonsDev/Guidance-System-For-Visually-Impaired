import numpy as np
import cv2
import time
import os

class YoloModel:
    def __init__(self, model_path, config_path, labels_path, confidence_threshold=0.5, nms_threshold=0.4):
        self.model_path = model_path
        self.config_path = config_path
        self.labels_path = labels_path
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        self.net = None
        self.classes = None
        self.layer_names = None
        self.output_layers = None
        self.colors = None
        self.load_model()

    def load_model(self):
        self.net = cv2.dnn.readNetFromDarknet(self.config_path, self.model_path)
        self.classes = []
        with open(self.labels_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        print(self.classes)
        self.layer_names = self.net.getLayerNames()
        unconnected_out_layers = self.net.getUnconnectedOutLayers()
        if unconnected_out_layers.ndim > 1:
            self.output_layers = [self.layer_names[i[0]-1] for i in unconnected_out_layers]
        else:
            self.output_layers = [self.layer_names[unconnected_out_layers[0]-1]]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        

    def detect_objects(self, image):
        model = cv2.dnn_DetectionModel(self.net)
        model.setInputParams(size=(125, 125), scale=1/255, swapRB=True)
        height, width, channels = image.shape
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416,416), (0,0,0), True, crop=False)
        self.net.setInput(blob)
        
        outs = self.net.forward(self.output_layers)
        class_ids = []
        confidences = []
        boxes = []
        class_ids, confidences, boxes = model.detect(image, self.confidence_threshold, self.nms_threshold)

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores) #Index of the class with the highest score
                confidence = scores[class_id] #Confidence of the class with the highest score
                if confidence > self.confidence_threshold:
                    # Object detected
                    center_x = int(detection[0]*width) #Center x of the object
                    center_y = int(detection[1]*height) #Center y of the object
                    w = int(detection[2]*width) #Width of the object
                    h = int(detection[3]*height) #Height of the object

                    # Rectangle coordinates
                    x = int(center_x - w/2) #Top left x
                    y = int(center_y - h/2) #Top left y

                    boxes.append([x, y, w, h])

                    print("Class ID: ", class_id, "Confidence: ", confidence, "position: ", center_x)

                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, self.nms_threshold)
        return boxes, confidences, class_ids, indexes
    
    def draw_boxes(self, image, boxes, confidences, class_ids, indexes):
        font = cv2.FONT_HERSHEY_SIMPLEX
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])
                confidence = str(int(confidences[i]*100))
                color = self.colors[i]
                cv2.rectangle(image, (x,y), (x+w, y+h), color, 2)
                cv2.putText(image, confidence, (x, y+30), font, 1, color, 2)
        return image
    
    def detect_and_draw(self, image):
        boxes, confidences, class_ids, indexes = self.detect_objects(image)
        return self.draw_boxes(image, boxes, confidences, class_ids, indexes)
    
    def detect_and_draw_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        while True:
            ret, frame = cap.read()
            if ret == False:
                break
            frame = self.detect_and_draw(frame)
            cv2.imshow("Image", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    model_path = "DeepLearning/Object_Detection/Yolo-darknet/yolov7-tiny.weights"
    config_path = "DeepLearning/Object_Detection/Yolo-darknet/yolov7-tiny.cfg"
    labels_path = "DeepLearning/Object_Detection/Yolo-darknet/coco.names"
    image_path = "DeepLearning/Object_Detection/Yolo-darknet/dogs.jpeg"
    video_path = 0
    yolo = YoloModel(model_path, config_path, labels_path)
    yolo.detect_and_draw_video(video_path)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
