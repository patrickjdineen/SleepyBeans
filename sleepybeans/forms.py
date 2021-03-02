from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email
from werkzeug.datastructures import MultiDict
from wtforms.fields.html5 import DateField

class UserSignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators= [DataRequired() ])
    first = StringField('First Name')
    last = StringField('Last Name')
    name = StringField('Name')
    submit_button = SubmitField()

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators= [DataRequired() ])
    submit_button = SubmitField()

class BabyForm(FlaskForm):
    name = StringField('Name')
    birthdate = DateField('Date')
    submit_button = SubmitField()
