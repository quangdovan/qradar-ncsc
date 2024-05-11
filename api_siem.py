import requests
from token_auth import token
import time

def qr_db():
    try:
        qradar_token, ncsc_token, sensor_id, vendor_id, unit_id, api_url, qradar_address = token()
    except:
        qradar_token = ncsc_token = sensor_id = vendor_id = unit_id = api_url = qradar_address = ""
    return qradar_token, ncsc_token, sensor_id, vendor_id, unit_id, api_url, qradar_address


def header(qradar_token):
    header = {
                'SEC':qradar_token,
                'Content-Type':'application/json',
                'accept':'application/json'
            }
    return header


def do_request_status(method, url, header):
    r = requests.request(method=method, url=url, headers=header, verify=False)
    return r.json(), r.status_code

def do_request(method, url, header):
    r = requests.request(method=method, url=url, headers=header, verify=False)
    return r.json()

def url_create_search(offense_id,event_count, condition, start, stop):
    url_create_search = f"""https://{qr_db()[6]}/api/ariel/searches?query_expression=select QIDNAME(qid) as 'Event Name',
    logsourcename(logSourceId) as 'Log Source',startTime AS 'Start Time',
    categoryname(category) as 'Low Level Category',"sourceIP" as 'Source IP',"sourcePort" as 'Source Port',
    "destinationIP" as 'Destination IP',"destinationPort" as 'Destination Port',"userName" as 'Username',
    "magnitude" as 'Magnitude', RULENAME(creeventlist) as 'Custom Rule',"eventDirection" as 'Direction',"severity" as 'Severity',
    PROTOCOLNAME(protocolid) as 'Protocol' from events where InOffense({offense_id}) and "severity" {condition} 
    order by "startTime" desc LIMIT {event_count} start '{start} 00:00' stop '{stop} 23:59'"""
    result = do_request('POST', url_create_search, header(qr_db()[0]))
    print(result)
    return result.get('search_id')

def url_result_search(id):
    url_result_search = f"https://{qr_db()[6]}/api/ariel/searches/{id}/results"
    while True:
        result, status_code = do_request_status('GET', url_result_search, header(qr_db()[0]))
        time.sleep(0.5)
        if status_code == 200:
            break
    print(result)
    return result.get('events')

def url_delete_search(id):
    url_delete_search = f"https://{qr_db()[6]}/api/ariel/searches/{id}"
    result = do_request('delete', url_delete_search, header(qr_db()[0]))
    return result
    
def check_location(ip):    
    url = f"""https://{qr_db()[6]}/api/services/geolocations?filter=ip_address='{ip}'"""
    result, status_code = do_request_status('get', url, header(qr_db()[0]))
    return result, status_code

def send_ncsc(data):
    response = requests.post(qr_db()[5], json=data)
    try:
        return response.status_code,response.json()
    except:
        return response.status_code,{"data":"null"}

