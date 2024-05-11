import sys
import os
current_directory = os.getcwd()

sys.path.append(current_directory)

from query_execute_database import execute,create_table


def create_db():
  create_table("""CREATE TABLE IF NOT EXISTS config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    qradar_ip TEXT NOT NULL,
    qradar_token TEXT NOT NULL,
    ncsc_token TEXT NOT NULL,
    sensor_id TEXT NOT NULL,
    vendor_id TEXT NOT NULL,
    unit_id TEXT NOT NULL,
    api_url TEXT NOT NULL,
    active INTEGER NOT NULL
  );""")

  create_table("""CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_config INTEGER NOT NULL,
    offense_id INTEGER NOT NULL,
    event_count INTEGER NOT NULL,
    event_send INTEGER NOT NULL,
    severity TEXT NOT NULL,
    query_time TEXT NOT NULL,
    time TEXT NOT NULL,
    FOREIGN KEY (id_config) REFERENCES config(id)
  );""")

create_db()
