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
			
	
	def run_config(self, config):
		job = config_dict[config]
		for pin in job['pins']:
			index = job['pins'].index(pin)
			spd = job['pins']['speeds'][index]
			timer = job['pins']['timers'][index]
			_thread.start_new_thread(self.move_servo, (pin, spd, timer))

	def service_run():
		rst = urllib.request.urlopen("http://andrewlewis.pythonanywhere.com/currentWall").read()
		rst = json.loads(rst.decode("utf-8"))	#bytes to string
		current_config = rst['currentWall']
