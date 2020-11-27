import sys
sys.path.append("/Users/nathanwaggoner/PlanterPi/")
#import pumps as p
#import db as db
#from planter import planter
from datetime import datetime
from sqltest import session, sensor_data, planter_config





class water_logic():
	def __init__(self):
		self.sensors = session.query(sensor_data).order_by(sensor_data.log_id.desc()).limit(24)
		self.planter = session.query(planter_config).first()
		m_count = 0
		moisture = 0
		self.avg_moisture = 0
		for s in self.sensors:
			m_count += 1
			moisture += s.soil_moisture
			self.avg_moisture = moisture/m_count



	def check_avg_moisture(self):

		if (self.avg_moisture > int(self.planter.target_moisture)):
			return 1
		else:
			return 0

	def update_cons_days(self):
		if (self.check_avg_moisture()):
			days_watered = int(self.planter.cons_days_watered) + 1
			#self.update_cons_days_watered(days_watered)
			#print(days_watered)
			self.planter.cons_days_watered = days_watered
			session.commit()
			return 1
		else:
			self.planter.cons_days_watered = 0
			session.commit()
			return 0

	def adj_run_time(self):
		if (int(self.planter.cons_days_watered) > 1):
			run_time = self.planter.run_time * .25 + self.planter.run_time
			self.planter.run_time = run_time
			session.commit()




#log = water_logic()

#print(log.adj_run_time())
