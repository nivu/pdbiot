
from flask import Flask, request, jsonify #added to top of file
from flask_cors import CORS #added to top of file
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
import sqlite3
from sensor_db import connect_to_db

def insert_sensor(sensor):
    inserted_sensor = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO sensors (analog, digital, battery, status) VALUES (?, ?, ?, ?)", (sensor['analog'],   
                    sensor['digital'], sensor['battery'], sensor['status']) )
        conn.commit()
        inserted_sensor = get_sensor_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()

    return inserted_sensor


sensor = {
    "analog": "10.5",
    "digital": "1",
    "battery": "100%",
    "status": "Good",
}

def get_sensors():
    sensors = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM sensors")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            sensor = {}
            sensor["sensor_id"] = i["sensor_id"]
            sensor["analog"] = i["analog"]
            sensor["digital"] = i["digital"]
            sensor["battery"] = i["battery"]
            sensor["status"] = i["status"]
            sensors.append(sensor)

    except:
        sensors = []

    return sensors

def get_sensor_by_id(sensor_id):
    sensor = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM sensors WHERE sensor_id = ?", 
                       (sensor_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        sensor["sensor_id"] = row["sensor_id"]
        sensor["analog"] = row["analog"]
        sensor["digital"] = row["digital"]
        sensor["battery"] = row["battery"]
        sensor["status"] = row["status"]
    except:
        sensor = {}

    return sensor


def update_sensor(sensor):
    updated_sensor = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE sensors SET analog = ?, digital = ?, battery = ?, status = ? WHERE sensor_id =?",  
                     (sensor["analog"], sensor["digital"], sensor["battery"], 
                     sensor["status"], sensor["sensor_id"],))
        conn.commit()
        #return the sensor
        updated_sensor = get_sensor_by_id(sensor["sensor_id"])

    except:
        conn.rollback()
        updated_sensor = {}
    finally:
        conn.close()

    return updated_sensor

def delete_sensor(sensor_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from sensors WHERE sensor_id = ?",     
                      (sensor_id,))
        conn.commit()
        message["status"] = "sensor deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete sensor"
    finally:
        conn.close()

    return message

@app.route('/api/sensors', methods=['GET'])
def api_get_sensors():
    return jsonify(get_sensors())

@app.route('/api/sensors/<sensor_id>', methods=['GET'])
def api_get_sensor(sensor_id):
    return jsonify(get_sensor_by_id(sensor_id))

@app.route('/api/sensors/add',  methods = ['POST'])
def api_add_sensor():
    sensor = request.get_json()
    return jsonify(insert_sensor(sensor))

@app.route('/api/sensors/update',  methods = ['PUT'])
def api_update_sensor():
    sensor = request.get_json()
    return jsonify(update_sensor(sensor))

@app.route('/api/sensors/delete/<sensor_id>',  methods = ['DELETE'])
def api_delete_sensor(sensor_id):
    return jsonify(delete_sensor(sensor_id))

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", debug=True)