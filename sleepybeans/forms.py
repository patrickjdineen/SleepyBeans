from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email
from werkzeug.datastructures import MultiDict
import datetime

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators= [DataRequired() ])
    first = StringField('First Name')
    last = StringField('Last Name')
    name = StringField('Name')
    birthdate = DateField('Date')
    submit_button = SubmitField()
