from query_execute_database import query
from create_db import create_db

if query("SELECT * FROM config") == None:
    create_db()

