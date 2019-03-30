from gpiozero import Button
import time
from send_email_with_att import email_sender as es


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
    

    
while True:
    if not button.is_pressed:
        print("HIGH")
        send_email()
    else:
        print("LOW")
    time.sleep(0.3)
