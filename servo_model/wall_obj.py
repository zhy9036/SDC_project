"""
# Yang Zhang
# import libs
"""
from enum import Enum
import _thread
import threading
import RPi.GPIO as GPIO
from time import sleep, time

class Action(Enum):
	OPEN = True
	CLOSE = False

class SDC_wall:
	default_max_config = 4
	default_config_dict = {1 : {'edge': ['a'], 'action':[Action.OPEN]},
					   2 : {'edge': ['b'], 'action':[Action.OPEN]},
					   3 : {'edge': ['c'], 'action':[Action.OPEN]},
					   4 : {'edge': ['a', 'b', 'c'], 'action':[Action.CLOSE, Action.CLOSE, Action.CLOSE]},}
	
	default_pin_list = [21, 20, 16, 19, 13, 6]
	default_edge_dict = {'a':{'pins':[21, 20], 'status': Action.CLOSE, 'speeds': [76, 115, 115, 75], 'timers': [3.3, 3.8, 1.5, 6]},
					 'b':{'pins':[16, 19], 'status': Action.CLOSE, 'speeds': [77, 115, 115, 75], 'timers': [3.3, 3.3, 1.8, 6]},
					 'c':{'pins':[13, 6], 'status': Action.CLOSE, 'speeds': [77, 115, 115, 76], 'timers': [3.1, 3.3, 0.8, 6]},
					 }

	
	def __init__(self, pin_list=default_pin_list, 
		edge_dict=default_edge_dict, config_dict=default_config_dict, 
		max_config=default_max_config):
		self.current_config = 0
		thread_list = []
		self.pin_list = pin_list
		self.edge_dict = edge_dict
		self.config_dict = config_dict
		self.max_config = max_config
		self.setup_GPIO(GPIO.BCM, self.pin_list)
		
		
	def __del__(self):
		self.cleanup_GPIO(self.pin_list)

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
			
			
	def gen_job_queue(self, config):
		job_queue = []
		if config > self.max_config or config < 0:
			return job_queue
		if config > self.current_config:
			job_queue = [k for k in range(self.current_config + 1, config + 1)]
		elif config < self.current_config:
			a = [k for k in range(self.current_config + 1, self.max_config+1)]
			b = [k for k in range(0, config+1)]
			job_queue = a + b
		return job_queue
		
		
	def reset(self):
		for edge in self.edge_dict:
			if self.edge_dict[edge]['status'] == Action.OPEN:
				self.edge_action(edge, Action.CLOSE)
		self.config = 0
		
		
	def exe_config(self, config):
		
		job_queue = self.gen_job_queue(config)
		if job_queue == []:
			print("No job to do, stand by...", end = '\r')
			return
		s_t = time.time()
		while(job_queue != []):
			if self.is_running():
				print("Wall is moving, config %d" % current_config, end='\r')
				continue
			cur = job_queue[0]
			job_queue = job_queue[1:]
			print("Executing config %d" % current_config, end='\r')
			if cur == 0: # resetting
				self.reset()
			else:
				edge_l = self.config_dict[cur]['edge']
				action_l = self.config_dict[cur]['action']
				for i in range(len(edge_l)):
					self.edge_action(edge_l[i], action_l[i])
				self.config = cur
				print("Wall updated to config %d" % self.config)
		e_t = time.time()
		print("Job finished in %f seconds" % (e_t - s_t))
				
		
	def is_running(self):
		self.thread_list = [t for t in self.thread_list if t.isAlive()]
		return self.thread_list != []


