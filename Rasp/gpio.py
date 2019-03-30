from gpiozero import Button
from time import sleep

button = Button(6)

while True:
    if not button.is_pressed:
        print("HIGH")
    else:
        print("LOW")
    sleep(0.3)
