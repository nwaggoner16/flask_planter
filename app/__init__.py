from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
import sys
sys.path.append('/home/pi/PlanterPi/')
from db import planter_by_id

app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)

from app import routes


global planter_obj
global user
global name
global hour_int
global avg_moisture
global avg_humidity
global get_sensor_data

planter_obj = planter_by_id(1)
user = {'username': 'Nathan'}
name = {'name': planter_obj.planter_name}
hour_int = 24
avg_moisture = {'moisture': planter_obj.avg_moisture(hour_int)}
avg_moisture_10 = {'moisture': planter_obj.avg_moisture(10)}
avg_humidity = {'humidity': planter_obj.avg_humidity()}
get_sensor_data = {'sensor_data': planter_obj.get_planter_sensor_data()}
