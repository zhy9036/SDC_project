"""
# Yang Zhang
# import libs
"""
from enum import Enum
import _thread
import threading
import urllib.request as req
from threading import Timer
import json
import RPi.GPIO as GPIO
from time import sleep, time

class Action(Enum):
	OPEN = True
	CLOSE = False

class SDC_wall:
	thread_list = []
	pin_list = [21, 20, 16, 19, 13, 6]
	edge_dict = {'a':{'pins':[21, 20], 'status': Action.CLOSE, 'speeds': [76, 115, 115, 75], 'timers': [3.3, 3.8, 1.5, 6]},
				 'b':{'pins':[16, 19], 'status': Action.CLOSE, 'speeds': [77, 115, 115, 75], 'timers': [3.3, 3.3, 1.8, 6]},
				 'c':{'pins':[13, 6], 'status': Action.CLOSE, 'speeds': [77, 115, 115, 76], 'timers': [3.1, 3.3, 0.8, 6]},
				 }

		
	def __init__(self):
		self.setup_GPIO(GPIO.BCM, SDC_wall.pin_list)
		
	def __del__(self):
		self.cleanup_GPIO(SDC_wall.pin_list)

	def setup_GPIO(self, mode, pins):
		GPIO.cleanup()
		GPIO.setmode(mode)
		GPIO.setwarnings(False)
		for pin in self.pin_list:
			GPIO.setup(pin, GPIO.OUT)
			
	def cleanup_GPIO(self, pins):
		for pin in self.pin_list:
			GPIO.output(pin, False)
		GPIO.cleanup()

	def move_servo(self, pin, speed, duration):
		pin_pwm =  GPIO.PWM(pin, 50)
		pin_pwm.start(0)
		duty = speed/ 18 + 2
		GPIO.output(pin, True)
		pin_pwm.ChangeDutyCycle(duty)
		sleep(duration)
		pin_pwm.ChangeDutyCycle(0)
		pin_pwm.stop()
		GPIO.output(pin, False)
		
		
	def edge_action(self, edge, action):
		if self.is_running():
			print('Model is running, waiting...', end='\r')
			return
		pins= self.edge_dict[edge]['pins']
		open_timer = self.edge_dict[edge]['timers'][:2]
		open_spd = self.edge_dict[edge]['speeds'][:2]
		close_timer = self.edge_dict[edge]['timers'][2:]
		close_spd = self.edge_dict[edge]['speeds'][2:]
		status = self.edge_dict[edge]['status']
		if action == Action.OPEN:
			if status == Action.OPEN:
				print('Try to open Edge %s, but edge %s already opened' % (edge, edge), end='\r')
				return
			#t1 = _thread.start_new_thread(self.move_servo, (pins[0], open_spd[0], open_timer[0]))
			#t2 = _thread.start_new_thread(self.move_servo, (pins[1], open_spd[1], open_timer[1]))
			t1 = threading.Thread(target=self.move_servo, args=(pins[0], open_spd[0], open_timer[0]))
			t2 = threading.Thread(target=self.move_servo, args=(pins[1], open_spd[1], open_timer[1]))
			t1.start()
			t2.start()
			self.thread_list.append(t1)
			self.thread_list.append(t2)
			self.edge_dict[edge]['status'] = Action.OPEN
		
		elif action == Action.CLOSE:
			if status == Action.CLOSE:
				print('Try to close Edge %s, but edge %s already closed' % (edge, edge), end='\r')
				return
			t1 = threading.Thread(target=self.move_servo, args=(pins[0], close_spd[0], close_timer[0]))
			t2 = threading.Thread(target=self.move_servo, args=(pins[1], close_spd[1], close_timer[1]))
			t1.start()
			t2.start()
			self.thread_list.append(t1)
			self.thread_list.append(t2)
			self.edge_dict[edge]['status'] = Action.CLOSE
			
	def is_running(self):
		self.thread_list = [t for t in self.thread_list if t.isAlive()]
		return self.thread_list != []


