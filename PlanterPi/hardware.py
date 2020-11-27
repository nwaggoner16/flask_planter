#!/usr/bin/python
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_dht

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
 
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
 
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
# Creaate dht object
dht = adafruit_dht.DHT11(board.D23)		

def read_light():
	light = 0
	ldr = AnalogIn(mcp, MCP.P0)
	while light == 0:
		try:
			light = ((ldr.value -65500)/(59000-65500))*100
		except RuntimeError as err:
			print('Handling Light Error')
			light = 0
	return light;
	
def read_soil_moisture():
	soil_moisture = 0
	soil_moisture_sensor = AnalogIn(mcp, MCP.P1)
	while soil_moisture == 0:
		try:
			soil_moisture = (soil_moisture_sensor.value - 55424)/(27900-55424)*100
		except RuntimeError as err:
			print('Handling Soil Moisture Error')
			soil_moisture = 0
	return soil_moisture;
	
def read_soil_temperature():
	soil_temperature_sensor = AnalogIn(mcp, MCP.P2)
	soil_temperature = 0
	while soil_temperature == 0:
		try:
			soil_temperature = soil_temperature_sensor.value
		except RuntimeError as err:
			print('Handling Soil Temp Error')
			soil_temperature = 0
	return soil_temperature;
	
def read_humidity():
	humidity = 0
	while humidity == 0:
		try:
			humidity = dht.humidity
		except RuntimeError as err:
			print('Handing humidity error')
			humidity = 0;
			
	return humidity;
	
def read_temperature():
	temperature = 0
	while temperature == 0:
		try:
			temperature =  dht.temperature * 9/5 + 32;
		except (RuntimeError, TypeError) as err:
			print('Handling RunTimeError')
			temperature = 0
			
	return temperature;
	
