import requests

def get_printer_json(serial):
	PRINTER_STATUS_ENDPOINT = 'http://pod0vg.eecs.berkeley.edu:3000/api/aprinters/job_data'
	headers = {'serial': str(serial)}
	r = requests.get(PRINTER_STATUS_ENDPOINT, headers=headers)
	return r.json()

def make_new_alert():
	return 'Making new alert!'