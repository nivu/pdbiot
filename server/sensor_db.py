import sqlite3

def connect_to_db():
    conn = sqlite3.connect('sensordatabase.db')
    return conn

def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE sensors (
                sensor_id INTEGER PRIMARY KEY NOT NULL,
                analog TEXT NOT NULL,
                digital TEXT NOT NULL,
                battery TEXT NOT NULL,
                status TEXT NOT NULL
            );
        ''')

        conn.commit()
        print("Sensor table created successfully")
    except:
        print("Sensor table creation failed - Maybe table")
    finally:
        conn.close()


create_db_table()