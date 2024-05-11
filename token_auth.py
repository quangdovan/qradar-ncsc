from query_execute_database import query
def token():
    result = query(f"""select qradar_token,ncsc_token,sensor_id, vendor_id, unit_id,api_url,qradar_ip from config where active=1 limit 1""")[0]
    qradar_token = result[0]
    ncsc_token = result[1]
    sensor_id = result[2]
    vendor_id = result[3]
    unit_id = result[4]
    api_url = result[5]
    qradar_address = result[6]
    return qradar_token, ncsc_token, sensor_id, vendor_id, unit_id, api_url, qradar_address


#qradar_token, ncsc_token, sensor_id, api_url, qradar_address = token()


