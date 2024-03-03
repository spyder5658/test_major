import cv2
from PIL import Image
import math
import numpy as np

from util import get_limits
import pyfirmata
import time

pin1=[8,9,10]
port="COM3"
board=pyfirmata.Arduino(port)

for i in pin1:
    board.digital[i].mode=pyfirmata.SERVO
    # board.digital[i].write(0)


# Function to move servo to a specific angle
def move_servo(angle):
    board.digital[8].write(angle)



cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
yellow = [0, 255, 255]  # yellow in BGR colorspace






while True:
    ret, frame = cap.read()
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(color=yellow)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    mask_ = Image.fromarray(mask)

  

    


    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox
        x_mid=(x1+x2)//2
        y_mid = (y1+y2)//2

        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        cv2.circle(frame,(x_mid,y_mid),5,(255,0,0),-1)
        X_distance = math.hypot(x_mid-0)
        Y_distance = math.hypot(y_mid-480)
        print(X_distance)
        cv2.line(frame,(0,480),(x_mid,y_mid),(0,0,255),5)
        cv2.line(frame,(640,480),(x_mid,y_mid),(0,0,255),5)
        X_distance=np.interp(X_distance,[0,600],[0,180]) #this line changes the distance into degrees of rotation
        Y_distance=np.interp(Y_distance,[0,480],[0,180]) #this line changes the distance into degrees of rotation
        print("X_distance is :",X_distance)
        move_servo(X_distance)  # Rotate the base
        print("Y_distance is :",Y_distance)     

    
   

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        break

cap.release()


cv2.destroyAllWindows()