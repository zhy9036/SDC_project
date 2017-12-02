"""
# Yang Zhang
# import libs
"""
import _thread
import urllib.request as req
from threading import Timer
import json
import RPi.GPIO as GPIO
from time import sleep, time

pin_list = [23]
speed_list = [90 for x in range(6)]
timer_list = [0 for x in rage(6)]
config_dict = {0:{'pins':pins, 'speeds': speed_list, 'timers': timer_list},
               1:{'pins':pins, 'speeds': speed_list, 'timers': timer_list},
               2:{'pins':pins, 'speeds': speed_list, 'timers': timer_list},
			   3:{'pins':pins, 'speeds': speed_list, 'timers': timer_list},
			   4:{'pins':pins, 'speeds': speed_list, 'timers': timer_list},
			   5:{'pins':pins, 'speeds': speed_list, 'timers': timer_list},
			   6:{'pins':pins, 'speeds': speed_list, 'timers': timer_list},}

def setup_GPIO(mode, pins):
	GPIO.setmode(mode)
	GPIO.setwarnings(False)
	for pin in pin_list:
		GPIO.setup(pin, GPIO.OUT)


def move_servo(pin, speed, duration):
	pin_pwm =  GPIO.PWM(pin, 50)
	pwm23.start(0)
	duty = speed/ 18 + 2
	GPIO.output(23, True)
	pin_pwm.ChangeDutyCycle(duty)
	sleep(duration)
	pwm23.ChangeDutyCycle(0)
	pin_pwm.stop()
	GPIO.output(pin, False)



def run_config(config):
	job = config_dict[config]
	for pin in job['pins']:
		index = job['pins'].index(pin)
		spd = job['pins']['speeds'][index]
		timer = job['pins']['timers'][index]
		_thread.start_new_thread(move_servo, (pin, spd, timer))

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def service_run():
	rst = urllib.request.urlopen("http://andrewlewis.pythonanywhere.com/currentWall").read()
	rst = json.loads(rst.decode("utf-8"))	#bytes to string
	current_config = rst['currentWall']

setup_GPIO(GPIO.BCM, pins)
#scheduler = RepeatedTimer(1, service_run)
s = time()
move_servo(23, 70, 1)
e = time()
print(e-s)
#sleep(1)
#GPIO.output(23, False)

#GPIO.cleanup()
