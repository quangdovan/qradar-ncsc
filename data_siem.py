def convertSeverity(number):
    if number >= 0 and number <= 2:
        return 1
    elif number >= 3 and number <= 5:
        return 2
    elif number >= 6 and number <= 7:
        return 3
    else:
        return 4

def directionP(direction):
    if direction == 'L2L':
        return 2
    elif direction == 'L2R':
        return 0
    else:
        return 1

def ConvertPort(port):
    if (port == 0):
        port = 9999
        return port
    else:
        return port

import check_location
from mitre_mapping import mitre_mapping

from api_siem import qr_db, send_ncsc

def parse_data(datas):
    count = 0
    print(datas)
    for data in datas:
        localtion = check_location.data_location(data.get('Source IP'))
        dataParse = {
                        "vendor_id": qr_db()[3],
                        "unit_id": qr_db()[4],
                        "sensor_id": '644203eb5f627d5469f1410d',
                        "timestamp": float(data.get('Start Time')),
                        "category": mitre_mapping(data.get('Custom Rule')),
                        "action": 3,
                        "signature": data.get('Event Name'),
                        "severity": convertSeverity(data.get('Severity')),
                        "direction": directionP(data.get('Direction')),
                        "dest_ip": data.get('Destination IP'),
                        "dest_port": ConvertPort(data.get('Destination Port')),
                        "src_ip":  data.get('Source IP'),
                        "src_port": ConvertPort(data.get('Source Port')),
                        "proto": data.get('Protocol'),
                        #"host": data.get('Source Asset Name'),
                        "host": "SOC-Console",
                        "tags": localtion['tags'],
                        "geoip" : {
                            "region_name": localtion['region_name'],
                            "timezone": localtion['timezone'],
                            "city_name": localtion['city_name'],
                            "lat": localtion['lat'],
                            "country_name": localtion['country_name'],
                            "lon": localtion['lon'],
                            "ip": data.get('Source IP'),
                            }
                        }
        print(dataParse)
        count += 1
        status_code, data = send_ncsc(dataParse)
    return status_code, count
 
