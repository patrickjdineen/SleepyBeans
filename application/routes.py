from application import app
from flask import render_template, request

from application.models import User, Baby, Sleep, check_password_hash

@app.route('/')
def home():
    return render_template('/pages/home.html')

@app.route('/sleep', methods= ['GET','POST'])
def sleep():
    if request.form:
        print(request.form)
    return render_template('/pages/sleep.html')