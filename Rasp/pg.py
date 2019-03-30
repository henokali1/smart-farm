import time
from time import time as t
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import serial
from ser_com_list import serial_ports as sp
from send_email_with_att import email_sender as es
import threading
import pickle


previous_time = 0.0
current_time = 0.0
email_delay = 60

leaf_current_time = 0.0
leaf_previous_time = 0.0
leaf_email = False

intruder_detected = False

print("Avalable port", sp()[0])

ser = serial.Serial(
    port=sp()[0],
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


def send_email(code):
    global current_time
    current_time = time.time()
    time_diff = current_time - previous_time
    if time_diff > email_delay:
        if code == 1:
            es(subject="Unhealthy Leaf Detected",
               message = "Unhealthy leaf has been detected. Please take a look at the image in the attachmet for further analysis.",
               file_location = 'unhealthy_leaf.png')
            global previous_time
            previous_time = current_time
        elif code == 2:
            es(subject="Unauthorized Intruder Has Been Detected",
               message = "Unauthorized intruder has been detected in the farm. Please take a look at the image in the attachmet for further analysis.",
               file_location = 'camera_current_image.png')
            global previous_time
            previous_time = current_time
            global intruder_detected
            intruder_detected = False
        
    else:
        print(time_diff)
        print("Wait a bit")


def ser_data():
    while 1:
        try:
            x=str(ser.readline(), 'utf-8').split(',')
            #print(x)
            if x[1] == 'p':
                print('PIR: {}'.format(x[0])) 
                if(x[0] != '-1'):
                    #print('PIR Location: {}'.format(x[0]))
                    global intruder_detected
                    intruder_detected = True
            
        except:
            print('ser err')



#Start Serial Thread
print('Starting Serail Thread')            
ser_thread = threading.Thread(name='ser_data', target=ser_data)
ser_thread.start()




#Define the threshold for finding a blue object with hsv
lower = pickle.load(open("lower.p", "rb" ))
upper = pickle.load(open("upper.p", "rb" ))
print('lower, upper', lower, upper)


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
    # grab the raw NumPy array representing the image, then initialize the timestamp
    frame = frame.array
    if(intruder_detected):
        print('intruder_detected: {}'.format(intruder_detected))
        global intruder_detected
        intruder_detected = False
        cv2.imwrite('camera_current_image.png', frame)
        send_email(code=2)

    # if not button.is_pressed:
    #     cv2.imwrite('camera_current_image.png', frame)
        
    #     print("HIGH")
    #     #send_email(code=2)
    # else:
    #     print("LOW")
    
    #Convert the frame in to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #Threshold HSV values for blue

    #Create binary image, where only blue colors apper in white and the rest will be in black
    mask = cv2.inRange(hsv, lower, upper)
    #Create Contours for the white pixles
    (_ ,contours, _) = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maximumArea = 0
    bestContour = None


    if len(contours) > 0:
            #currentArea = cv2.contourArea(contour)
        #bestContour = contour
        #maximumArea = currentArea
        bestContour = sorted(contours, key = cv2.contourArea, reverse = True)[0]
    #Draw a bounding box around the largest white pixles
        
        if bestContour is not None:
            x,y,w,h = cv2.boundingRect(bestContour)
            area = cv2.contourArea(bestContour)
            cv2.rectangle(frame, (x,y),(x+w,y+h), (0,0,255), 3)
            M = cv2.moments(bestContour)
            (cX, cY) = (int(M["m10"] / (M["m00"] + 0.00001)), int(M["m01"] / (M["m00"] + 0.00001)))
            (startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
            (startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
            cv2.line(frame, (startX, cY), (endX, cY), (0, 0, 255), 3)
            cv2.line(frame, (cX, startY), (cX, endY), (0, 0, 255), 3)
            leaf_current_time = t()
            # send_email(code=1)
            #Get the center of the bounding box (it's center)
            pos_x = int(M['m10']/(M['m00'] + 0.00001))
            pos_y = int(M['m01']/(M['m00'] + 0.00001))


            if(leaf_current_time - leaf_previous_time > 30) and (area > 100):
                cv2.imwrite('unhealthy_leaf.png', frame)
                leaf_previous_time = t()
                global leaf_email
                leaf_email = True
                print('send email')

                send_email(code=1)
            else:
                print('Leaf Email delay')
                    
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
cv2.destroyAllWindows()

