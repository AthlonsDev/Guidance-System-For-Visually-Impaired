import cv2
import numpy as np
from Speech import Speech
import time
import threading as th

np.random.seed(20) # set the seed for numpy for reproducibility
class Detector:
    label = ""
    def __init__(self, videoPath, configPath, modelPath, classesPath):
        self.videoPath = videoPath
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath

        self.net = cv2.dnn.readNetFromTFLite(self.modelPath)
        # self.net = cv2.dnn.DetectionModel(self.modelPath, self.configPath) # load the model
        self.net.setInputSize(220, 220) # set the input size of the image to 320x320, the lower the faster the inference
        self.net.setInputScale(1.0 / 127.5) # set the input scale to 1/127.5 (255/2)
        self.net.setInputMean((127.5, 127.5, 127.5)) # set the mean of the input to 127.5
        self.net.setInputSwapRB(True) # set the swapRB to True to swap the first and last channel of the image

        self.readClasses()

    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()

        self.classesList.insert(0, "__background__")

        self.colorList = np.random.uniform(0, 255, size=(len(self.classesList), 3)) # generate random colors for each class

        print(self.classesList)

    def runDetection(self, bboxIdx, confidences, bboxs, image, classLabelIds, i):
            bbox = bboxs[np.squeeze(bboxIdx[i])] # get the bbox
            classConfidence = confidences[np.squeeze(bboxIdx[i])] # get the confidence
            classLabelId = np.squeeze(classLabelIds[np.squeeze(bboxIdx[i])]) # get the class label id
            classLabel = self.classesList[classLabelId] # get the class label
            classColor = [int(c) for c in self.colorList[classLabelId]] # get the class color

            displayText = "{}: {:.2f}".format(classLabel, classConfidence) # display text with 2 decimal places for the confidence

            x, y , w, h = bbox # get the bbox coordinates

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2) # draw the bbox rectangle 
            cv2.putText(image, displayText, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, classColor, 1) # draw the text

            linewidth = min(int(w * 0.3), int(h * 0.3)) # line is 30% of the width and height of the bbox

            cv2.line(image, (x, y), (x + linewidth, y), classColor, thickness=4) # draw the top left line
            cv2.line(image, (x, y), (x, y + linewidth), classColor, thickness=4) # draw the top left line
            cv2.line(image, (x + w, y), (x + w - linewidth, y), classColor, thickness=4) # draw the top right line
            cv2.line(image, (x + w, y), (x + w, y + linewidth), classColor, thickness=4) # draw the top right line
            cv2.line(image, (x, y + h), (x + linewidth, y + h), classColor, thickness=4) # draw the bottom left line
            cv2.line(image, (x, y + h), (x, y + h - linewidth), classColor, thickness=4) # draw the bottom left line
            cv2.line(image, (x + w, y + h), (x + w - linewidth, y + h), classColor, thickness=4) # draw the bottom right line
            cv2.line(image, (x + w, y + h), (x + w, y + h - linewidth), classColor, thickness=4) # draw the bottom right line

            self.label = classLabel   
            return self.label

    def onVideo(self):
        cap = cv2.VideoCapture(self.videoPath) 

        if not cap.isOpened():
            print("Error opening video stream or file")
            return
        (success, image) = cap.read() 

        while success:
            classLabelIds, confidences, bboxs = self.net.detect(image, confThreshold=0.5) # 0.5 is the confidence threshold

            bboxs = list(bboxs) # convert to list 
            confidences = list(np.array(confidences).reshape(1, -1)[0]) # convert to list and reshape 
            confidences = list(map(float, confidences)) # convert to float 

            bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold=0.7, nms_threshold=0.2) # 0.5 is the confidence threshold, 0.3 is the nms threshold

            if len(bboxIdx) != 0: # if there is a detection
                for i in range(0, len(bboxIdx)): # for each detection 
                    self.label = self.runDetection(bboxIdx, confidences, bboxs, image, classLabelIds, i)
                    #run speech in a separate thread
                    speech = Speech()
                    t = th.Thread(target=speech.say, args=(self.label,))
                    t.start()
                    t.join()
                    print(self.label)
                    time.sleep(3)


                    
                

            cv2.imshow("Output", image)


            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
 
            (success, image) = cap.read()

            
        cv2.destroyAllWindows()

        