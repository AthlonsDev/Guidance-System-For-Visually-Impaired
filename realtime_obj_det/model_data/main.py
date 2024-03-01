from Detector import *
# from Speech import *
import os

def main():
<<<<<<< HEAD
    videoPath = "/home/athlons/Documents/Final_Project/realtime_obj_det/test_videos/video-2.mp4"
=======
    videoPath = "realtime_obj_det/test_videos/traffic.mp4"
>>>>>>> a9cf953 (fixes)
    # videoPath = 0
    #to use it on the webcam, set the videoPath to 0
    # speech = Speech()

<<<<<<< HEAD
    coco = "/home/athlons/Documents/Final_Project/realtime_obj_det/model_data/coco.names"
    mobilenetv3 = "/home/athlons/Documents/Final_Project/realtime_obj_det/model_data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
    mobilenetv2 = "/home/athlons/Documents/Final_Project/realtime_obj_det/model_data/mobilenet_v2.pb"
    yolo5 = "/home/athlons/Documents/Final_Project/realtime_obj_det/model_data/yolov-5.tflite"
    frozen_inference = "/home/athlons/Documents/Final_Project/realtime_obj_det/model_data/frozen_inference_graph.pb"

    configPath = os.path.join(mobilenetv3)
    print(configPath)
    modelPath = os.path.join(mobilenetv2) 
=======
    configPath = os.path.join("realtime_obj_det/model_data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    print(configPath)
    modelPath = os.path.join("realtime_obj_det/model_data/frozen_inference_graph.pb") 
>>>>>>> a9cf953 (fixes)
    print(modelPath)
    if not os.path.isfile(modelPath):
        print(f"Model file does not exist: {modelPath}")
    else:
        print(f"Model file exists: {modelPath}")

<<<<<<< HEAD
    classesPath = os.path.join(coco)
=======
    classesPath = os.path.join("realtime_obj_det/model_data/coco.names")
>>>>>>> a9cf953 (fixes)
    print(classesPath)

    detector = Detector(videoPath, yolo5, configPath, classesPath)
    # # run detector on one thread
    detector.onVideo()
    print(detector.label)

    # #read file to get distance
    # path = "../Pico(W) Remote Workspace/distance.txt"
    # f = open(path, "r")
    # distance = f.read()
    # f.close()

    # print(distance)


    # speech.say(inputText)



if __name__ == "__main__":
    
    main()
