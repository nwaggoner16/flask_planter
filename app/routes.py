from flask import render_template, flash, redirect
from app import app
import sys
sys.path.append('/home/pi/PlanterPi/')
from planter import planter
from db import general_data, planter_by_id, cursor
from app.forms import LoginForm, PlanterForm, Planter_name_list, HoursForm, WaterForm
import pumps


#planter_name = ''
global planter_obj
#gl_planter_id = planter_obj.planter_id
#planter_obj = planter(planter_name)
'''@app.route('/planter_page', methods=['GET', 'POST'])
def planter_page():

	form = PlanterForm()
	
	if form.validate_on_submit():
		
		planter_name = form.plantername.data
		flash('Planter {} selected'.format(planter_name))
		return redirect('/data/{}'.format(planter_name))
	
	return render_template('planter.html', title='Planter', form=form)'''
	
	
@app.route('/', methods=['GET', 'POST'])
@app.route('/planter_list_page', methods=['GET', 'POST'])
def planter_list_page():

	form = Planter_name_list()
	global planter_obj
		
	if form.validate():
		global planter_obj
		planter_id = form.planternamelist.data
		planter_obj = planter_by_id('{}'.format(planter_id))
		
		
		#flash('Planter {} selected'.format(planter_id))
		return redirect('/data_hours/{}/24'.format(planter_id))
	
	return render_template('planter_list.html', title='Planter', form=form)

'''
@app.route('/data/<planter_id>')
@app.route('/data/<planter_id>', methods=['GET', 'POST'])
def data(planter_id):
	planter_obj = planter_by_id('{}'.format(planter_id))
	#planter_obj = planter('Demeter')
	user = {'username': 'Nathan'}
	name = {'name': planter_obj.planter_name}
	avg_moisture = {'moisture': planter_obj.avg_moisture()}
	avg_moisture_10 = {'moisture': planter_obj.avg_moisture(10)}
	avg_humidity = {'humidity': planter_obj.avg_humidity()}
	get_sensor_data = {'sensor_data': planter_obj.get_planter_sensor_data()}
	hour_form = HoursForm()
	if hour_form.validate():
		hour_val = hour_form.hours.data
		return redirect('/data_hours/{}/{}'.format(planter_obj.planter_id, hour_val))
	return render_template('index.html', title='Planter', user=user, avg_moisture=avg_moisture, avg_moisture_10=avg_moisture_10, avg_humidity=avg_humidity, get_sensor_data=get_sensor_data, name=name, hour_form=hour_form)#, planter_object = planter_obj)
'''
@app.route('/data_hours/<planter_id>/<hours>')
@app.route('/data_hours/<planter_id>/<hours>', methods=['GET', 'POST'])
def data_hours(planter_id, hours=24):
	global planter_obj
	#planter_obj = planter_by_id('{}'.format(planter_id))
	#planter_obj = planter('Demeter')
	user = {'username': 'Nathan'}
	name = {'name': planter_obj.planter_name}
	hour_int = int(hours)
	avg_moisture = {'moisture': planter_obj.avg_moisture(hour_int)}
	avg_moisture_10 = {'moisture': planter_obj.avg_moisture(10)}
	avg_humidity = {'humidity': planter_obj.avg_humidity()}
	get_sensor_data = {'sensor_data': planter_obj.get_planter_sensor_data()}
	print(get_sensor_data)
	hour_form = HoursForm()
	if hour_form.validate():
		hour_val = hour_form.hours.data
		return redirect('/data_hours/{}/{}'.format(planter_id, hour_val))
	return render_template('index.html', title='Planter', user=user, avg_moisture=avg_moisture, avg_moisture_10=avg_moisture_10, avg_humidity=avg_humidity, get_sensor_data=get_sensor_data, name=name, hour_form=hour_form)#, planter_object = planter_obj)

@app.route('/water_control')
@app.route('/Water_control', methods=(['GET', 'POST']))
def water_control():
	water_form = WaterForm()
	global planter_obj
	name = {'name': planter_obj.planter_name}
	return render_template('water_control.html', name=name)
	
