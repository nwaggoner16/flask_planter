import paho.mqtt.client as mqtt
from sqltest import sensor_data_raw, session, mqtt_test
import json
from ast import literal_eval
from datetime import datetime


planter_id_var = 0
temperature_var = 0
humidity_var = 0
light_var = 0
soil_temperature_var = 0
soil_moisture_var = 0

def json_insert(sensor_json):
    print(sensor_json)
    print(sensor_json.get('planter_id'))
    #planter_id_var = int(sensor_json.get('planter_id'))
    #temperature_var = int(sensor_json.get('temperature'))
    #humidity_var = int(sensor_json.get('humidity'))
    #light_var = int(sensor_json.get('light'))
    #soil_temperature_var = int(sensor_json.get('soil_temperature'))
    #soil_moisture_var = int(sensor_json.get('soil_moisture'))
    #print(type(planter_id_var))
    #print(planter_id_var)
    #print(temperature_var)

    sensor_insert = mqtt_test(
        log_time = datetime.now(),
        planter_id=int(sensor_json.get('planter_id')),
        temperature=float(sensor_json.get('temperature'))*9/5 + 32,
        humidity=float(sensor_json.get('humidity')),
        pressure=int(sensor_json.get('pressure')),
        gas_resistance=int(sensor_json.get('gas_resistance')),
        altitude=float(sensor_json.get('altitude')),
        soil_temperature=int(sensor_json.get('soil_temperature')),
        soil_moisture=int(sensor_json.get('soil_moisture')),
        ir=int(sensor_json.get('IR')),
        full=int(sensor_json.get('Full')),
        visible=int(sensor_json.get('Visible')),
        lux=float(sensor_json.get('Lux'))
    )
    print(sensor_json.get('temperature'))
    
    session.add(sensor_insert)
    session.commit()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("test/mqtt_test")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    sensor_data_m = str(msg.payload.decode("utf-8","ignore"))
    
    sensor_object = literal_eval(sensor_data_m)
    print(sensor_object)
    json_insert(sensor_object)
     

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.28")
#client.publish("test/mqtt_test", "mac")

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
