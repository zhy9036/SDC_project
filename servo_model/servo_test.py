from tkinter import *
import RPi.GPIO as GPIO
import pigpio
import time

pi = pigpio.pi()
pi.set_mode(21, pigpio.OUTPUT)
pi.set_PWM_frequency(21, 50)
#pi.set_mode(21, pigpio.INPUT)
#pi.stop()
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(21, GPIO.OUT)
#pwm = GPIO.PWM(21, 50)
#pwm.start(5)

class App:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        scale = Scale(frame, from_=0, to=180,
              orient=HORIZONTAL, command=self.update)
        scale.grid(row=0)


    def update(self, angle):
        #duty = float(angle) / 18+ 2
        #pwm.ChangeDutyCycle(duty)
        #pi.set_PWM_dutycycle(21, duty)
        pw = 1000 + int(float(angle) * 5.56)
        print(pw)
        pi.set_servo_pulsewidth(21, pw)

root = Tk()
root.wm_title('Servo Control')
app = App(root)
root.geometry("200x50+0+0")
root.mainloop()
