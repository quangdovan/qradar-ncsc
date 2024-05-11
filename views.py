from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
import sqlite3
from query_execute_database import query,execute
from data_siem import parse_data
import api_siem
import check_db
import query_execute_database

viewsbp = Blueprint('viewsbp', __name__, url_prefix='/')

@viewsbp.route('/')
@viewsbp.route('/index')
def index():
    return render_template('index.html')



data2 = [{"offense_id": "2", "events": "abcd-efgh-qwer-rtyu", "severity": "abcd-efgh-qwer-rtyu", "query": "https://ncsc.gov.vn/api/v3","time": "02/01/2024 10:00:00","active":1},
         {"offense_id": "1", "events": "abcd-efgh-qwer-rtyu", "severity": "abcd-efgh-qwer-rtyu", "query": "https://ncsc.gov.vn/api/v3","time": "02/01/2024 10:00:00", "active":0}]
@viewsbp.route('/history/<int:page>')
def history(page):
    data = [dict(id=row[0],id_config=row[1], offense_id=row[2], event_count=row[3], event_send=row[4], severity=row[5], query_time=row[6], time=row[7],qradar_ip=row[8]) for row in query('SELECT h.*,c.qradar_ip FROM history h JOIN config c ON h.id_config = c.id order by time DESC')]
    per_page = 5
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    sliced_data = data[start_index:end_index]

    total_entries = len(data)
    total_pages = (total_entries + per_page - 1) // per_page

    return render_template('history.html', data=sliced_data, total_pages=total_pages, current_page=page,total_entries=total_entries)

@viewsbp.route('/config/<int:page>')
def config(page):
    data = [dict(id=row[0],qradar_ip=row[1], qradar_token=row[2], ncsc_token=row[3],sensor_id=row[4], vendor_id=row[5], unit_id=row[6], api_url=row[7], active=row[8]) for row in query("""SELECT * FROM 'config' order by id desc""")]
    per_page = 5
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    sliced_data = data[start_index:end_index]

    total_entries = len(data)
    total_pages = (total_entries + per_page - 1) // per_page
    return render_template('config.html', data=sliced_data, total_pages=total_pages, current_page=page,total_entries=total_entries)


@viewsbp.route('/send', methods=['POST'])
def send():
    query1 = query_execute_database.query(f"""select id,api_url from config where active=1 limit 1""")[0]
    id_config = query1[0]
    id_offense = request.form['id']
    event_count = request.form['event_count']
    severity = request.form['severity']
    start = request.form['from']
    stop = request.form['to']
    query_time = start + ' => ' + stop
    qradar_address = query1[1]
    
    id_search = api_siem.url_create_search(id_offense, event_count, severity, start, stop)

    data = api_siem.url_result_search(id_search)

    status_code, event_sent  = parse_data(data)
    if status_code == 200:
        api_siem.url_delete_search(id_search)
        value = (id_config, id_offense, event_count, event_sent, severity, query_time)
        query = "INSERT INTO history (id_config, offense_id, event_count, event_send, severity, query_time, time) VALUES (?, ?, ?, ?, ?, ?, strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))"
        execute(query, value)
        return f"""<script>alert("Đã gửi thành công"); window.location.href = '{url_for('viewsbp.index')}';</script>"""
    else:
        return f"""<script>alert("Gửi không thành công"); window.location.href = '{url_for('viewsbp.index')}';</script>"""
    
#Delete history
@viewsbp.route('/delete', methods=['POST'])
def delete():
    ids = request.json
    ids = str(ids).replace("[","").replace("]","")
    placeholders = ', '.join('?' for _ in ids)
    print(placeholders)
    query = f"DELETE FROM history WHERE id IN ({placeholders})"
    execute(query, ids)
    return f"{id}<br>"



#Add Token
@viewsbp.route('/config/addToken', methods=['POST'])
def add():
    qradar_address = request.form['qradar_address']
    qradar_token = request.form['qradar_token']
    ncsc_token = request.form['ncsc_token']
    sensor_id = request.form['sensor_id']
    vendor_id = request.form['vendor_id']
    unit_id = request.form['unit_id']
    api_url = request.form['api_url']
    value = (qradar_address, qradar_token, ncsc_token, sensor_id, vendor_id, unit_id, api_url, 0)
    query = "INSERT INTO config (qradar_ip, qradar_token, ncsc_token, sensor_id, vendor_id, unit_id, api_url, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    execute(query, value)
    return redirect(url_for('viewsbp.config', page=1), code=303)

#Edit Token
@viewsbp.route('/config/editToken', methods=['POST'])
def editToken():
    qradar_address = request.form['qradar_address']
    qradar_token = request.form['qradar_token']
    ncsc_token = request.form['ncsc_token']
    sensor_id = request.form['sensor_id']
    api_url = request.form['api_url']
    data_id = request.form['employee_id']
    query="""UPDATE config SET qradar_ip=?, qradar_token=?, ncsc_token=?, sensor_id=?, api_url=? WHERE id=?"""
    value = (qradar_address, qradar_token, ncsc_token, sensor_id, api_url, data_id)
    execute(query, value)
    return redirect(url_for('viewsbp.config', page=1), code=303)

#Delete Token
@viewsbp.route('/deleteToken', methods=['POST'])
def deleteToken():
    ids = request.json
    placeholders = ', '.join('?' for _ in ids)
    query = f"DELETE FROM config WHERE id IN ({placeholders})"
    execute(query, ids)  
    return redirect(url_for('viewsbp.config', page=1), code=303)

#Active Token
@viewsbp.route('/update_config', methods=['POST'])
def update_config():
    config_id = request.form.get('config_id')
    active = request.form.get('active')
    query ="UPDATE config SET active = ? WHERE id = ?"
    value = (active, config_id)
    execute(query, value)
    query_set_active_0 = "UPDATE config SET active = ? WHERE id != ?"
    value_set_active_0 = (0, config_id)
    execute(query_set_active_0, value_set_active_0)
    return 'Cập nhật thành công'

@viewsbp.route('/about')
def about():
    return render_template('about.html')

app = Flask(__name__)
app.register_blueprint(viewsbp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)

