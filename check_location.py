from api_siem import check_location

def data_location(ip):
    datas, status = check_location(ip)
    if status != 404:
        for data in datas:
            result = {  
                    "tags": 1,
                    "region_name": data.get('city').get('name'),
                    "timezone": data.get('location').get('timezone'),
                    "city_name": data.get('city').get('name'),
                    "country_name": data.get('physical_country').get('name'),
                    "lat": data.get('location').get('latitude'),
                    "lon": data.get('location').get('longitude'),
                    "ip": data.get('ip_address')
        }
    else:
         result = {  
                    "tags": 1,
                    "region_name": "Hanoi",
                    "timezone": "Asia/Bangkok",
                    "city_name": "Hanoi",
                    "country_name": "Vietnam",
                    'lat': 21.0313, 
                    'lon': 105.8516,
                    "ip": ip
        }
    return result
