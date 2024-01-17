#Control camera

import cv2 # import opencv 
import numpy as np # import numpy

cap = cv2.VideoCapture(0) # capture video from camera

#adjust depth of field
focus = 25 # min: 0, max: 255, increment:5
key = cv2.CAP_PROP_FOCUS
cap.set(key, focus) # set the focus 


cap.set(3, 840) # set the width
cap.set(4, 680) # set the height
cap.set(10, 100) # set the brightness
cap.set(11, 50) # set the contrast
cap.set(12, 50) # set the saturation
cap.set(13, 13) # set the hue
cap.set(14, 50) # set the gain
cap.set(15, -3) # set the exposure
cap.set(16, 50) # set the white balance

while True:
    ret, frame = cap.read() # read the frame
    cv2.imshow("frame", frame) # show the frame
    if cv2.waitKey(1) & 0xFF == ord('q'): # if q is pressed, exit
        break






cap.release() # release the camera
cv2.destroyAllWindows() # destroy all windows