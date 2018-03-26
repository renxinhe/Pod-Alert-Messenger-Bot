import json
import requests

PRINTER_STATUS_ENDPOINT = 'http://pod0vg.eecs.berkeley.edu:3000/api/aprinters/job_data'
PRINTER_SERIALS = ["10094", "10097", "10098", "10213", "10453", "10454", "10025", "10026", "10034", "10035", "10038", "10047"]

def get_printer_raw(serial):
    headers = {'serial': str(serial)}
    if str(serial) not in PRINTER_SERIALS:
        return None
    r = requests.get(PRINTER_STATUS_ENDPOINT, headers=headers)
    if r.status_code == 200:
        try:
            return r.content
        except ValueError as e:
            print 'Failed to decode JSON for printer %s: %s' % (serial, r.content)
            return None
    else:
        return None

def get_printer_json(serial):
    headers = {'serial': str(serial)}
    if str(serial) not in PRINTER_SERIALS:
        return None
    r = requests.get(PRINTER_STATUS_ENDPOINT, headers=headers)
    if r.status_code == 200:
        try:
            return r.json()
        except ValueError as e:
            print 'Failed to decode JSON for printer %s: %s' % (serial, r.content)
            return None
    else:
        return None

def get_all_printer_json():
    all_status = []
    for serial in PRINTER_SERIALS:
        printer_json = get_printer_json(serial)

        printer_status = {}
        printer_status['serial'] = serial
        printer_status['print_name'] = '--'
        printer_status['progress'] = ''
        printer_status['progress_color'] = 'bg-primary'
        printer_status['time_remaining'] = '--'
        printer_status['state'] = '--'

        if printer_json is not None and printer_json.get('errno') is None:
            try:
                printer_status['print_name'] = printer_json['job']['file']['name'].rstrip('.gcode')

                progress = printer_json['progress']['completion']
                if progress is not None:
                    printer_status['progress'] = '%.1f' % (printer_json['progress']['completion'])
                if printer_json['progress']['completion'] == 100.0:
                    printer_status['progress_color'] = 'bg-success'

                seconds_remaining = printer_json['progress']['printTimeLeft']
                if seconds_remaining is not None:
                    printer_status['time_remaining'] = '%d:%02d:%02d' %\
                        (seconds_remaining // 3600, 
                         seconds_remaining // 60 % 60, 
                         seconds_remaining % 60)

                printer_status['state'] = printer_json['state']
            except KeyError as e:
                print 'Error parsing printer %s info: %s' % (serial, e)
        else:
            printer_status['progress'] = '100.0'
            printer_status['progress_color'] = 'bg-danger'

            if printer_json is not None:
                errno = printer_json.get('errno')
                if errno == 'EHOSTUNREACH':
                    printer_status['state'] = 'Printer unreachable'
                elif errno == 'ENOTFOUND':
                    printer_status['state'] = 'Printer number not found'

        all_status.append(printer_status)
    print json.dumps(all_status)
    return json.dumps(all_status)

def make_new_alert():
    return 'Making new alert!'