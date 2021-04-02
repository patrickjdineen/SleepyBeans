from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Email
from werkzeug.datastructures import MultiDict
from wtforms.fields.html5 import DateField

class UserSignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators= [DataRequired() ])
    first = StringField('First Name' , validators= [DataRequired() ])
    last = StringField('Last Name' , validators= [DataRequired() ])
    submit_button = SubmitField()

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators= [DataRequired() ])
    submit_button = SubmitField()

class BabyForm(FlaskForm):
    name = StringField('Name' , validators= [DataRequired() ])
    birthdate = DateField('Date', validators= [DataRequired() ])
    submit_button = SubmitField()

class UpdateForm(FlaskForm):
    name = StringField('Name')
    birthdate = DateField('Date')
    submit_button = SubmitField()

class SleepForm(FlaskForm):
    sleep_choices= ['Nap','Bedtime']
    sleep_type=SelectField('Sleep Type', choices=sleep_choices, validators= [DataRequired() ])
    submit_button=SubmitField()