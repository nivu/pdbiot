from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_to_db():
    conn = sqlite3.connect('sensordatabase.db')
    return conn

def insert_sensor(sensor):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO sensors (analog, digital, battery, status) VALUES (?, ?, ?, ?)", (sensor['analog'],   
                    sensor['digital'], sensor['battery'], sensor['status']) )
        conn.commit()
    except:
        conn().rollback()

    finally:
        conn.close()

    return "success"

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

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/api/sensors/<sensor_id>', methods=['GET'])
def api_get_sensor(sensor_id):
    print(sensor_id)
    return "data is " + str(sensor_id)

@app.route('/api/sensors/', methods=['GET'])
def api_get_sensor_query():
    args = request.args
    print(args['id'])
    return args

@app.route('/api/sensors/add',  methods = ['POST'])
def api_add_sensor():
    sensor = request.get_json()
    return insert_sensor(sensor)

@app.route('/api/sensors', methods=['GET'])
def api_get_sensors():
    return jsonify(get_sensors())

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", debug=True)