from sleepybeans import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from sleepybeans.models import User, Baby, Sleep, check_password_hash
from sleepybeans.forms import UserLoginForm

@app.route('/')
def home():
    return render_template('/home.html')



@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User(email_address = email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect (url_for('login'))
    return render_template('/signup.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = UserLoginForm()
    print(form.data)
    if request.method =='POST':
        email=email.form.data
        print(email)
        password = password.form.data
        logged_user = User.query.filter(User.email_address == email).first()
        #NOTE FOR FUTURE. QUEURY.LAST COULD BE USED FOR MOST RECENT NAP???
        if logged_user and check_password_hash(logged_user.password,password):
            login_user(logged_user)
            return redirect(url_for('profile'))
    return render_template('/login.html', form=form)

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    return render_template('/profile.html')

@app.route('/sleep', methods= ['GET','POST'])
def sleep():
    if request.form:
        print(request.form)
    return render_template('/sleep.html')