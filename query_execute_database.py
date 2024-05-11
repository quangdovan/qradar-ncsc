import sqlite3

def query(value):
    try:
        conn = sqlite3.connect("./database/store.db")
        cur = conn.cursor()
        cur.execute(value)
        result = cur.fetchall()
        return result
    except sqlite3.Error as e:
        print("Lỗi SQLite:", e)
        return None
    finally:
        cur.close()  # Đóng con trỏ
        conn.close()  # Đóng kết nối


def execute(query, values):
    try:
        conn = sqlite3.connect("./database/store.db")
        cur = conn.cursor()
        cur.execute(query, values)
        print("Dữ liệu đã được chèn hoặc cập nhật thành công")
        conn.commit()
    except sqlite3.Error as e:
        print("Lỗi SQLite:", e)
    finally:
        cur.close()
        conn.close()

def create_table(value):
    try:
        conn = sqlite3.connect("./database/store.db")
        cur = conn.cursor()
        cur.execute(value)
    except sqlite3.Error as e:
        print("Lỗi SQLite:", e)
    finally:
        cur.close()
        conn.close()  # Đóng kết nối

