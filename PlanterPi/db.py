import mysql.connector as mariadb
import configparser
import numpy
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from matplotlib.figure import Figure

#import io


#Initializing config object
config = configparser.ConfigParser()
config.read("/Users/nathanwaggoner/PlanterPi/config.ini")

#Getting db connection info
host = config.get('credentials','host')
user = config.get('credentials','user')
passwd = config.get('credentials','passwd')
db = config.get('credentials','db')

#Initializing db connection
mysql = mariadb.connect(user=user, password=passwd, database=db)
cursor = mysql.cursor()

class planter():
	def __init__(self, planter_name):
		#Setting planter variables
		self.planter_header = self.get_planter_header_data(planter_name)
		self.planter_name = planter_name
		self.planter_id = self.planter_header[0]
		self.cons_days_watered = self.planter_header[2]
		#self.times_watered = self.planter_header[3]
		self.planter_sensor_data = self.get_planter_sensor_data(self.planter_id)
		self.run_speed = self.planter_header[4]
		self.run_time = self.planter_header[5]
		self.target_moisture = self.planter_header[6]

	def get_planter_header_data(self, planter_name):
		#Getting planter header info from planter table using planter_name
		temp_query = "SELECT planter_id, planter_name, cons_days_watered, run_speed, run_time, target_moisture FROM PlanterPi.planter WHERE planter_name = '{}';".format(planter_name)
		cursor.execute(temp_query)

		#Declaring numpy array to store header info
		planter_header = []
		for arr in cursor:
			planter_header = arr

		planter_header = numpy.array(planter_header)

		return planter_header;

	def get_planter_sensor_data(self, planter_id):
		#Getting planter sensor data
		sensor_data_query = "SELECT planter_id, log_id, log_time, temperature, humidity, light, soil_temperature, soil_moisture FROM PlanterPi.sensor_data WHERE planter_id = {};".format(planter_id)
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
		cursor.execute('insert into PlanterPi.water_log (planter_id, run_time_sec, run_speed) values ({}, {}, {})'.format(self.planter_id, run_time, run_speed))
		mysql.commit()


class planter_by_id():
	def __init__(self, planter_id):
		#Setting planter variables
		self.planter_header = self.get_planter_header_data(planter_id)
		self.planter_name = self.planter_header[1]
		self.planter_id = planter_id
		self.cons_days_watered = self.planter_header[2]
		#self.times_watered = self.planter_header[3]
		self.planter_sensor_data = self.get_planter_sensor_data()
		self.run_speed = self.planter_header[3]
		self.run_time = self.planter_header[4]
		self.target_moisture = self.planter_header[5]

	def get_planter_header_data(self, planter_id):
		#Getting planter header info from planter table using planter_name
		temp_query = "SELECT planter_id, planter_name, cons_days_watered, run_speed, run_time, target_moisture FROM PlanterPi.planter WHERE planter_id = {};".format(planter_id)
		cursor.execute(temp_query)

		#Declaring numpy array to store header info
		planter_header = []
		for arr in cursor:
			planter_header = arr

		planter_header = numpy.array(planter_header)

		return planter_header;

	def get_planter_sensor_data(self):
		#Getting planter sensor data
		sensor_data_query = "SELECT planter_id, log_id, log_time, temperature, humidity, light, soil_temperature, soil_moisture FROM PlanterPi.sensor_data WHERE planter_id = {};".format(self.planter_id)
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
			temperature_sum += p[3];
		temperature_avg =  temperature_sum/hours
		return temperature_avg

	def avg_humidity(self, hours=24):
		humidity_sum = 0
		humidity_avg = 0
		last_hours_h = self.planter_sensor_data[-hours:]
		last_hours_h_np = numpy.array(last_hours_h)
		for p in last_hours_h_np:
			humidity_sum += p[4];
		humidity_avg =  humidity_sum/hours
		return humidity_avg

	def avg_light(self, hours=24):
		light_sum = 0
		light_avg = 0
		last_hours_h = self.planter_sensor_data[-hours:]
		last_hours_h_np = numpy.array(last_hours_h)
		for p in last_hours_h_np:
			light_sum += p[5];
		light_avg =  light_sum/hours
		return light_avg

	def avg_soil_temperature(self, hours=24):
		soil_temperature_sum = 0
		soil_temperature_avg = 0
		last_hours_h = self.planter_sensor_data[-hours:]
		last_hours_h_np = numpy.array(last_hours_h)
		for p in last_hours_h_np:
			soil_temperature_sum += p[6];
		soil_temperature_avg =  soil_temperature_sum/hours
		return soil_temperature_avg

	def update_cons_days_watered(self, days):
		cursor.execute('update planter set cons_days_watered = {} where planter_id = {}'.format(days, self.planter_id))
		mysql.commit()

	def water_logging(self, run_time, run_speed):
		cursor.execute('insert into PlanterPi.water_log (planter_id, run_time_sec, run_speed) values ({}, {}, {})'.format(self.planter_id, run_time, run_speed))
		mysql.commit()

	def update_run_time(self, rt):
		cursor.execute('update planter set run_time = {} where planter_id = {}'.format(rt, self.planter_id))
		self.run_time = rt

	def update_run_speed(self, rs):
		cursor.execute('update planter set run_speed = {} where planter_id = {}'.format(rs, self.planter_id))

	def plot_moisture_data(self, hours):
		plot_array_time = []
		cursor.execute('select log_time from sensor_data where planter_id = {} order by log_time desc limit={};'.format(self.planter_id, hours))
		for n in cursor:
			plot_array_time.append(n[0])

		plot_array_moisture = []
		cursor.execute('select soil_moisture from sensor_data where planter_id = {} order by log_time desc limit={};'.format(self.planter_id, hours))
		for n in cursor:
			plot_array_moisture.append(n[0])

		return (plot_array_time), (plot_array_moisture)

	def plot_moisture_data_test(self, hours):
		plot_array_time = []
		plot_array_moisture=[]
		plot_var_time = self.planter_sensor_data[-hours:]
		#plot_array_moisture = self.planter_sensor_data[-hours:]
		for pl in plot_var_time:
			plot_array_time.append(pl[2])
			plot_array_moisture.append(pl[7])
		return (plot_array_time), (plot_array_moisture)

	def get_log_times(self):
		return self.planter_sensor_data[:, 2]

	def get_soil_moisture(self):
		return self.planter_sensor_data[:, 7]

	def get_temperature(self):
		return self.planter_sensor_data[:, 3]

	def get_soil_temperature(self):
		return self.planter_sensor_data[:, 6]



class general_data():
	def get_planter_names(self):
		planter_name_arr = []
		cursor.execute('select distinct cast(planter_id as varchar(50)), planter_name from planter order by planter_name asc;')
		for n in cursor:
			planter_name_arr.append(n)
		return planter_name_arr




# DEBUG
rongo = planter_by_id(2)
print(rongo.get_soil_moisture())
#debug_ob = general_data()
#print(debug_ob.get_planter_names())
