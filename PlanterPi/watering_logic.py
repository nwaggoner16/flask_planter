import sys
sys.path.append("/home/pi/PlanterPi/")
import pumps as p
import db as db
from datetime import datetime

demeter_sensors = db.planter('Demeter')
rongo_sensors = db.planter('Rongo')

demeter_moisture = demeter_sensors.avg_moisture()
rongo_moisture = rongo_sensors.avg_moisture()
pumps = p.l298n(22, 15, 18,7,12,11)


print(datetime.now());

if(demeter_moisture < 55):
	run_time = 15
	run_speed = 75
	pumps.pump1(run_speed, run_time);
	print('    ran pump 1');
	print('    Demeter Moisture: ' + str(demeter_moisture));
	days_watered = int(rongo_sensors.cons_days_watered)
	days_watered += 1
	demeter_sensors.update_cons_days_watered(days_watered)
	demeter_sensors.water_logging(15, 75)
	
else:
	print('    did not run pump 1');
	print('    Demeter Moisture: ' + str(demeter_moisture));
	demeter_sensors.update_cons_days_watered(0)
	
if(rongo_moisture < 55):
	run_time = 15
	run_speed = 75
	pumps.pump2(run_speed, run_time);
	print('    ran pump 2');
	print('    Rongo Moisture: ' + str(rongo_moisture));
	days_watered = int(demeter_sensors.cons_days_watered)
	days_watered += 1
	rongo_sensors.update_cons_days_watered(days_watered)
	rongo_sensors.water_logging(15, 75)
else:
	print('    did not run pump 2');
	print('    Rongo Moisture: ' + str(rongo_moisture));
	rongo_sensors.update_cons_days_watered(0)

pumps.cleanup()
