from gpiozero import Button
import time
from send_email_with_att import email_sender as es
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np

button = Button(6)

previous_time = 0.0
current_time = 0.0
email_delay = 60

def send_email():
    global current_time
    current_time = time.time()
    time_diff = current_time - previous_time
    if time_diff > email_delay:
        es()
        global previous_time
        previous_time = current_time
    else:
        print(time_diff)
        print("Wait a bit")
    




#Define the threshold for finding a blue object with hsv
lower = np.array([95, 150, 75])
upper = np.array([145, 255, 255])
a = np.array([95, 150, 75])
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    if not button.is_pressed:
        print("HIGH")
        send_email()
    else:
        print("LOW")
    time.sleep(0.3)
    # grab the raw NumPy array representing the image, then initialize the timestamp
    frame = frame.array
    #Convert the frame in to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #Threshold HSV values for blue
    lower_blue = np.array([95, 150, 75])
    upper_blue = np.array([145, 255, 255])
    #Create binary image, where only blue colors apper in white and the rest will be in black
    mask = cv2.inRange(hsv, lower, upper)
    #Create Contours for the white pixles
    (_ ,contours, _) = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maximumArea = 0
    bestContour = None
    
    
            
    if(np.array_equal(lower, [95, 150, 75]) and len(contours) == 0):
        lower = np.array([160,150,75])
        upper = np.array([180,255,255])
    elif(np.array_equal(lower, [160,150,75]) and len(contours) == 0):
        lower = np.array([95, 150, 75])
        upper = np.array([145, 255, 255])

    if len(contours) > 0:
            #currentArea = cv2.contourArea(contour)
        #bestContour = contour
        #maximumArea = currentArea
        bestContour = sorted(contours, key = cv2.contourArea, reverse = True)[0]
    #Draw a bounding box around the largest white pixles
        
        if bestContour is not None:
            x,y,w,h = cv2.boundingRect(bestContour)
            cv2.rectangle(frame, (x,y),(x+w,y+h), (0,0,255), 3)
            M = cv2.moments(bestContour)
            (cX, cY) = (int(M["m10"] / (M["m00"] + 0.00001)), int(M["m01"] / (M["m00"] + 0.00001)))
            (startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
            (startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
            cv2.line(frame, (startX, cY), (endX, cY), (0, 0, 255), 3)
            cv2.line(frame, (cX, startY), (cX, endY), (0, 0, 255), 3)
            cv2.imwrite('unhealthy_leaf.png', frame)    
            #Get the center of the bounding box (it's center)
            pos_x = int(M['m10']/(M['m00'] + 0.00001))
            pos_y = int(M['m01']/(M['m00'] + 0.00001))
                    
    #Display the commands on the screen
    #cv2.putText(frame, onScreen, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0, 0, 255), 2)
    # show the frame
    cv2.imshow("Frame", frame)
    #cv2.imshow("Binary", mask)
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
cv2.waitKey()
