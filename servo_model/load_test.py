import requests, time

def reset_model():
	headers = {'Content-type': 'application/json'}
	rst = requests.post("http://andrewlewis.pythonanywhere.com/currentWall/", 
		headers = headers, json={'currentWall': '0', 'deviceID': '-1'})

iteration = 0
while True:
	headers = {'Content-type': 'application/json'}
	rst = requests.post("http://andrewlewis.pythonanywhere.com/currentWall/", 
		headers = headers, json={'currentWall': '4', 'deviceID': '-1'})
	if rst.status_code == 201:
		iteration += 1
		print('testing... %d' % iteration, end = '\r')
		time.sleep(30)
	else:
		break
	headers = {'Content-type': 'application/json'}
	rst = requests.post("http://andrewlewis.pythonanywhere.com/currentWall/", 
		headers = headers, json={'currentWall': '0', 'deviceID': '-1'})
	time.sleep(1)
