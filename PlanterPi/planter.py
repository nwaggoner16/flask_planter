from db import cursor, mysql
import numpy

class planter():
	def __init__(self, planter_name):
		#Setting planter variables
		self.planter_header = self.get_planter_header_data(planter_name)
		self.planter_name = planter_name
		self.planter_id = self.planter_header[0]
		self.cons_days_watered = self.planter_header[2]
		self.times_watered = self.planter_header[3]
		self.planter_sensor_data = self.get_planter_sensor_data(self.planter_id)
		self.run_speed = self.planter_header[4]
		self.run_time = self.planter_header[5]
		self.target_moisture = self.planter_header[6]
	
	def get_planter_header_data(self, planter_name):	
		#Getting planter header info from planter table using planter_name
		temp_query = "SELECT planter_id, planter_name, cons_days_watered, times_watered, run_speed, run_time, target_moisture FROM Plant_logger.planter WHERE planter_name = '{}';".format(planter_name)
		cursor.execute(temp_query)
		
		#Declaring numpy array to store header info
		planter_header = []
		for arr in cursor:
			planter_header = arr
			
		planter_header = numpy.array(planter_header)
			
		return planter_header;

	def get_planter_sensor_data(self, planter_id):
		#Getting planter sensor data
		sensor_data_query = "SELECT planter_id, log_id, log_time, temperature, humidity, light, soil_temperature, soil_moisture FROM Plant_logger.sensor_data WHERE planter_id = {};".format(planter_id)
		cursor.execute(sensor_data_query)
		
		#Storing sensor data into numpy array
		planter_sesnor_data = []
		for row in cursor:
			planter_sesnor_data.append(row);	
				
		planter_array_np = numpy.array(planter_sesnor_data)
		
		return planter_array_np

	def avg_moisture(self, hours=24):
		moisture_sum = 0
		moisture_avg = 0
		last_hours_m = self.planter_sensor_data[-hours:]
		last_hours_m_np = numpy.array(last_hours_m)
		for p in last_hours_m_np:
			moisture_sum += p[7];
		moisture_avg =  moisture_sum/hours
		return moisture_avg
		
	def avg_temperature(self, hours=24):
		temperature_sum = 0
		temperature_avg = 0
		last_hours_temp = self.planter_sensor_data[-hours:]
		last_hours_temp_np = numpy.array(last_hours_temp)
		for p in last_hours_temp_np:
			temperature_sum += p[7];
		temperature_avg =  temperature_sum/hours
		return temperature_avg	
	
	def avg_humidity(self, hours=24):
		humidity_sum = 0
		humidity_avg = 0
		last_hours_h = self.planter_sensor_data[-hours:]
		last_hours_h_np = numpy.array(last_hours_h)
		for p in last_hours_h_np:
			humidity_sum += p[7];
		humidity_avg =  humidity_sum/hours
		return humidity_avg

	def update_cons_days_watered(self, days):
		cursor.execute('update planter set cons_days_watered = {} where planter_id = {}'.format(days, self.planter_id))
		mysql.commit()
		
	def water_logging(self, run_time, run_speed):
		log_curs.execute('insert into water_log (planter_id, run_time, run_speed) values ({}, {}, {})'.format(self.planter_id, run_time, run_speed))
		mysql.commit()
		
	def update_run_time(self, run_time):
		cursor.execute('update planter set run_time = {} where planter_id = {}'.format(run_time, self.planter_id))
		mysql.commit()
		
	def update_target_moisture(self, target_moisture):
		cursor.execute('update planter set target_moisture = {} where planter_id = {}'.format(target_moisture, self.planter_id))
		mysql.commit()
		
		
	#print(self.planter_name)
	
#log = water_logic('Demeter')

#print(log.planter_name)
