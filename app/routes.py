from flask import render_template, flash, redirect, Response, request
from app import app
import sys
sys.path.append('/home/pi/PlanterPi/')
from planter import planter
from db import general_data, planter_by_id, cursor
from app.forms import LoginForm, PlanterForm, Planter_name_list, HoursForm, WaterForm, ChartForm
import pumps
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure



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
		
		#flash('Planter {} selected'.format(planter_id))
		return redirect('/data_hours/{}/24'.format(planter_id))
		#return redirect('/plot.png/{}'.format(planter_id))
	
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
	global user
	global name
	global hour_int
	global avg_moisture
	global avg_moisture_10
	global avg_humidity
	global get_sensor_data
	#planter_obj = planter_by_id('{}'.format(planter_id))
	#planter_obj = planter('Demeter')
	
		
	
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
	return render_template('water_control.html', name=name)
	
@app.route('/plot.png')
def plot_png():
	global planter_obj
	fig = create_figure()
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')
	
def create_figure():
	global planter_obj
	global hour_int
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	plot_arr = planter_obj.plot_moisture_data_test(hour_int)
	print(plot_arr)
	axis.plot(plot_arr[0], plot_arr[1])
	return fig
	
	
