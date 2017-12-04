from wall_obj import *
import requests
import urllib.request as req
from threading import Timer
import json
curent_config = 0
wall = SDC_wall()

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
		

def run_config(config):
	job = config_dict[config]
	for pin in job['pins']:
		index = job['pins'].index(pin)
		spd = job['pins']['speeds'][index]
		timer = job['pins']['timers'][index]
		_thread.start_new_thread(self.move_servo, (pin, spd, timer))

def reset_model():
	headers = {'Content-type': 'application/json'}
	rst = requests.post("http://andrewlewis.pythonanywhere.com/currentWall/", 
		headers = headers, json={'currentWall': '0', 'deviceID': '-1'})
	return rst.status_code


def service():
	rst = req.urlopen("http://andrewlewis.pythonanywhere.com/currentWall").read()
	rst = json.loads(rst.decode("utf-8"))	#bytes to string
	current_config = rst['currentWall']
	wall.job_queue == []:
		wall.exe_config(current_config)
	#print(current_config)
def run():
	print('Resetting...', end='\r')
	code = reset_model()	
	if code != 201:
		print('Resetting faild! Error response code %d'%code)
		return
	wall.reset()
	print('Resetting... Successed! reset to 0', end='\r\n')
	scheduler = RepeatedTimer(1, service)

	
run()

