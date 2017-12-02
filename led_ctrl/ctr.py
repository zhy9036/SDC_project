# imported libs
import _thread as thd
import urllib.request
from threading import Timer
import json
import RPi.GPIO as GPIO
import time

pin_arry = [14, 15, 18]
pre = 0
running_light = False
running_blink = False
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

def setupRPi(pins):
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	for pin in pins:
		GPIO.setup(pin, GPIO.OUT)

def resetRPi():
	GPIO.cleanup()

def light_up(pins, duration):
	global running_light
		#if GPIO.input(pin) == 0:
	running_light = True
	GPIO.output(pins, GPIO.HIGH)
	time.sleep(duration)
	GPIO.output(pins, GPIO.LOW)
	running_light = False

def blink(pins, duration, initial):
	global running_blink
	running_blink = True
	cur = time.time()
	while cur - initial < duration:
		GPIO.output(pins, GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(pins, GPIO.LOW)
		time.sleep(0.1)
		cur = time.time()	
	running_blink = False

def exe_config(current_config):
	global pre, running_blink, running_light
	if current_config == 0:
		pre = 0
		GPIO.output(pin_arry, GPIO.LOW)
		print('Model reset', end='\r\n')
	elif current_config in range(1, 6):
		if not running_blink and not running_light:
			if pre == current_config - 1:
				job_light = thd.start_new_thread(light_up, (pin_arry[pre], 3))
				job_blink = thd.start_new_thread(blink, ([x for x in pin_arry if not x==pin_arry[pre]], 3, time.time()))
				pre = current_config
				print('updated: ',current_config, end='\r')
			else:
				print('wrong order: ', 'should be %d' % (pre + 1), 'but recieving %d' % current_config, end='\r')
		else:
			print('running ...', running_blink, running_light, end='\r')
	else:
		print('unknow config %d' % current_config, end = '\r')
			 
			 
def getEvent():
	global pre, running_blink, running_light
	rst = urllib.request.urlopen("http://andrewlewis.pythonanywhere.com/currentWall").read()
	
	rst = json.loads(rst.decode("utf-8"))	#bytes to string
	current_config = rst['currentWall']
	
	exe_config(current_config)
	"""
	if current_config == pre:
		GPIO.output(18, GPIO.HIGH)
	else:
		GPIO.output(18, GPIO.LOW)
	
	
	if current_config == 0:
		pre = 0
		GPIO.output(pin_arry, GPIO.LOW)
	elif current_config == 1:
		if not running_blink and not running_light:
			if pre == 0:
				pre = current_config
				job_light = thd.start_new_thread(light_up, ([pre-1], 3))
				job_blink = thd.start_new_thread(blink, ([x for x in pin_arry if not x==pre-1], 3, time.time()))
				print('updated: ',current_config)
				#if not running:
				#	running = True
				#	job_light.run()
				#job_light.run()
				#job_blink.run()
			else:
				print('Wrong order')
		else:
			print('running ...', running_blink, running_light, end='\r')
	elif current_config == 2:
		if pre == 1:
			pre = current_config
			print('updated: ',current_config)
		else:
			GPIO.output(18, GPIO.LOW)
			print('Wrong order')
	else:
		GPIO.output(18, GPIO.LOW)
		print("unknown config", current_config)
	"""

#getEvent()

#setupRPi([18])
#GPIO.output(18, GPIO.HIGH)
#time.sleep(3)
#GPIO.output(18, GPIO.LOW)

setupRPi([18, 15, 14])
scheduler = RepeatedTimer(1, getEvent)

