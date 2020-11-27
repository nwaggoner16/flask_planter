import sys
sys.path.append("/Users/nathanwaggoner/PlanterPi/")
#import pumps as p
#import db as db
from datetime import datetime
from sqltest import session, sensor_data, planter_config
from watering import water_logic

log = water_logic()

#If calling for water adding 1 to the cons_days_watered
log.update_cons_days()
#If watering 2 days in a row increase run time by 25%
log.adj_run_time()

#Prints log data and runs pump if needed
if(log.check_avg_moisture()):
	log_file = open("water_log.txt", "a")
	log_time = str(datetime.now())
	log_moisture = str(log.avg_moisture)
	log_file.write(log_time)
	log_file.write(log_moisture)
	log_file.close()
	#pumps.pump1()
