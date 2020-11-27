#!/usr/bin/python
#import sys
#sys.path.append('/home/pi/PlanterPi/')
#import hardware as hw
from datetime import datetime
from sqltest import session, sensor_data, sensor_data_raw


temperature = 75 #hw.read_temperature()
humidity = 58 #hw.read_humidity()
light = 69 #hw.read_light()
soil_temperature = 74 #hw.read_soil_temperature()
soil_moisture = 55 #hw.read_soil_moisture()

print(datetime.now())
print('	Temperature: ' + str(temperature))
print('	Humidity: ' + str(humidity))
print('	Light: ' + str(light))
print('	Soil Temp: ' + str(soil_temperature))
print('	Soil Moisture: ' + str(soil_moisture))

sensor_insert = sensor_data(
	planter_id=1,
	temperature=temperature,
	humidity=humidity,
	light=light,
	soil_temperature=soil_temperature,
	soil_moisture=soil_moisture
)
sensor_insert_raw = sensor_data_raw(
	planter_id=1,
	temperature=temperature,
	humidity=humidity,
	light=light,
	soil_temperature=soil_temperature,
	soil_moisture=soil_moisture
)

session.add(sensor_insert)
session.add(sensor_insert_raw)
session.commit()
