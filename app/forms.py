from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectField, IntegerField
from wtforms.validators import DataRequired
import db

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Submit')

class PlanterForm(FlaskForm):
	plantername = StringField('Planter Name', validators=[DataRequired()])
	submit = SubmitField('Go')

class Planter_name_list(FlaskForm):
	planter_data = db.general_data()
	planter_names = planter_data.get_planter_names()
	planternamelist = SelectField(label= 'Planter', choices = planter_names)
	submit = SubmitField('Submit')

class HoursForm(FlaskForm):
	hours = IntegerField('Time Frame', validators=[DataRequired()])
	time_option = SelectField(label='Time Frame', choices = [('1', 'Hours'),('2', 'Days')])
	submit = SubmitField('Submit')

class WaterForm(FlaskForm):
	rt_input = IntegerField('Run Time')
	rs_input = IntegerField('Run Speed')
	water_trig = SubmitField('Water Now')
	
class ChartForm(FlaskForm):
	view_chart = SubmitField('View Chart')
