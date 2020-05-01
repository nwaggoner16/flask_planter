from flask import render_template, flash, redirect, Response, request
from app import app
import sys
sys.path.append('/home/pi/PlanterPi/')
from planter import planter
from db import general_data, planter_by_id, cursor
from app.forms import LoginForm, PlanterForm, Planter_name_list, HoursForm, WaterForm, ChartForm, PlantLogForm
import pumps

global planter_obj

	
@app.route('/', methods=['GET', 'POST'])
@app.route('/planter_list_page', methods=['GET', 'POST'])
def planter_list_page():

	form = Planter_name_list()
	global planter_obj
		
	if form.validate():
		global planter_obj
		global user
		global name
		global hour_int
		global avg_moisture
		global avg_moisture_10
		global avg_humidity
		global get_sensor_data
		planter_id = form.planternamelist.data
		planter_obj = planter_by_id('{}'.format(planter_id))
		user = {'username': 'Nathan'}
		name = {'name': planter_obj.planter_name}
		hour_int = int(24)
		avg_moisture = {'moisture': planter_obj.avg_moisture(hour_int)}
		avg_moisture_10 = {'moisture': planter_obj.avg_moisture(10)}
		
		avg_humidity = {'humidity': planter_obj.avg_humidity()}
		get_sensor_data = {'sensor_data': planter_obj.get_planter_sensor_data()}
		
	
		return redirect('/data_hours/{}/24'.format(planter_id))
		
	
	return render_template('planter_list.html', title='Planter', form=form)


@app.route('/data_hours', methods=['GET', 'POST'])
@app.route('/data_hours/<planter_id>/<hours>', methods=['GET', 'POST'])
def data_hours(planter_id=1, hours=24):
	global planter_obj
	global user
	global name
	global hour_int
	global avg_moisture
	global avg_moisture_10
	global avg_humidity
	global get_sensor_data
	planter_id = planter_obj.planter_id
	
		
	
	hour_form = HoursForm()
	chart_form = ChartForm()
	if hour_form.validate():
		global hour_int
		global avg_moisture
		if hour_form.time_option.data=='1':
			global hour_int
			global avg_moisture
			hour_int = hour_form.hours.data
			avg_moisture = {'moisture': planter_obj.avg_moisture(hour_int)}
			return redirect('/data_hours/{}/{}'.format(planter_id, hour_int))
		elif hour_form.time_option.data=='2':
			
			hour_int = hour_form.hours.data*24
			avg_moisture = {'moisture': planter_obj.avg_moisture(hour_int)}
			return redirect('/data_hours/{}/{}'.format(planter_id, hour_int))
		
	if chart_form.validate():
		return redirect('/plot.png')
	return render_template('index.html', title='Planter', user=user, avg_moisture=avg_moisture, avg_moisture_10=avg_moisture_10, avg_humidity=avg_humidity, get_sensor_data=get_sensor_data, name=name, hour_form=hour_form, chart_form=chart_form)#, planter_object = planter_obj)
	
@app.route('/water_control')
@app.route('/Water_control', methods=(['GET', 'POST']))
def water_control():
	water_form = WaterForm()
	global planter_obj
	name = {'name': planter_obj.planter_name}
	
	if water_form.validate():
		global run_time
		global run_speed
		run_time = water_form.rt_input.data
		run_speed = water_form.rs_input.data
		print(run_time)
		print(run_speed)
	return render_template('water_control.html', name=name, water_form=water_form)
	
@app.route('/plant_log', methods=(['GET','POST']))
def plant_log():
	plant_log_form = PlantLogForm()
	global planter_obj
	name = {'name': planter_obj.planter_name}
	
	if plant_log_form.validate():
		planter_obj.plant_log_form(plant_log_form.browning.data, plant_log_form.plant_tags.data, plant_log_form.plant_notes.data)
		return redirect('/plant_log')
	return render_template('plant_log.html', title='Plant Log', name=name, plant_log_form=plant_log_form)
	
	
