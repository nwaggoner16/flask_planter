import paho.mqtt.client as mqtt
import json


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("test/mqtt_test")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
sensor_set='"planter_id:1", "temperature:55", "humidity:55", "light:55", "soil_temperature:55", "soil_moisture:55"'

sensor_dict = dict(planter_id = "1", temperature = "55", humidity = "55", light = "55", soil_temperature = "55", soil_moisture = "55")
sensor_json = json.dumps(sensor_dict)
print(sensor_json)

sensor_insert = "sensor_data_raw(planter_id=1, temperature=55, humidity=55, light=55, soil_temperature=55, soil_moisture=55)"
client.connect("192.168.1.28")
client.publish("test/mqtt_test", sensor_json)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()


void loop() {
 
  StaticJsonBuffer<300> JSONbuffer;
  JsonObject& JSONencoder = JSONbuffer.createObject();
 
  JSONencoder["planter_id"] = 1;
  JSONencoder["temperature"] = 75;
  JSONencoder["humidity"] = 75;
  JSONencoder["light"] = 75;
  JSONencoder["soil_temperature"] = 75;
  JSONencoder["soil_moisture"] = 75;

 
  char JSONmessageBuffer[100];
  JSONencoder.printTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
  Serial.println("Sending message to MQTT topic..");
  Serial.println(JSONmessageBuffer);
 
  if (client.publish("test/mqtt_test", JSONmessageBuffer) == true) {
    Serial.println("Success sending message");
  } else {
    Serial.println("Error sending message");
  }
 
  client.loop();
  Serial.println("-------------");
 
  delay(10000);
 
}