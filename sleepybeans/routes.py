from sleepybeans import app, db, login_manager
from flask import render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime

from sleepybeans.models import User, Baby, Sleep, check_password_hash
from sleepybeans.forms import UserLoginForm, DateField, UserSignUpForm, BabyForm, SleepForm


#TBD
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#Home
@app.route('/')
def home():
    return render_template('/home.html')

#Sign Up Page
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        first = form.first.data
        last = form.last.data
        user = User(email_address = email, password=password, first_name = first,last_name=last)
        db.session.add(user)
        db.session.commit()
        return redirect (url_for('login'))
    return render_template('/signup.html', form=form)

# Log In Page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = UserLoginForm()
    print(form.data)
    if request.method =='POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        logged_user = User.query.filter(User.email_address == email).first()
        print(logged_user)
        #NOTE FOR FUTURE. QUEURY.LAST COULD BE USED FOR MOST RECENT NAP???
        if logged_user and check_password_hash(logged_user.password,password):
            login_user(logged_user)
            return redirect(url_for('profile'))
    return render_template('/login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    if session:
        for key in list(session.keys()):
            session.pop(key)
    return redirect(url_for('login'))


#home profile page - TODO finish
@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    baby = "test static baby"
    parent_id = current_user.token
    babies = Baby.query.filter(Baby.parent_id== current_user.token).all()
    user = User.query.filter(User.token==current_user.token).first()
    return render_template('/profile.html',
    babies = babies, user=user)
    # first_name = user.first_name,
    # baby_name=baby.name,
    # baby_birthdate=baby.birth_date)

#Page to create baby and commit them to DB
@app.route('/baby', methods= ['GET','POST'])
@login_required
def new_baby():
    form = BabyForm()
    if request.method == 'POST':
        name = form.name.data
        date=form.birthdate.data
        new_baby = Baby(name=name, birth_date=date, parent_id=current_user.token)
        db.session.add(new_baby)
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        print("fail")
    return render_template('/baby.html',form=form)

#route to remove baby from list of babies
@app.route('/baby/<baby_id>', methods= ['GET','DELETE'])
@login_required
def del_baby(baby_id):
    baby=Baby.query.filter_by(id=baby_id).first()
    if not baby:
        print('failed')
    db.session.delete(baby)
    db.session.commit()
    return redirect(url_for('profile'))
#route to update a baby
@app.route('/baby/<baby_id>/update', methods=['GET','POST','PUT'])
@login_required
def update_baby(baby_id):
    baby=Baby.query.filter_by(id=baby_id).first()
    form = BabyForm()
    if request.method == 'POST':
        baby.name = form.name.data
        baby.birth_date=form.birthdate.data
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        return render_template('/baby.html',form=form)

@app.route('/baby/<baby_id>/sleep', methods=['GET','POST'])
@login_required
def main_sleep(baby_id):
    form=SleepForm()
    sleeps = Sleep.query.filter_by(child_id=baby_id).all()
    baby= Baby.query.filter_by(id=baby_id).first()
    if request.method=='GET':
        return render_template('/sleep.html', sleeps=sleeps, baby=baby, form=form)
    if request.method=='POST':
        sleep_type=form.sleep_type.data
        start_time=datetime.utcnow()
        sleep = Sleep(sleep_type=sleep_type,child_id=baby.id,start_time=start_time, end_time=None, sleep_duration=None)
        db.session.add(sleep)
        print(sleep)
        db.session.commit()
        return redirect(url_for('main_sleep', form=form, sleeps=sleeps, baby_id=baby.id))

@app.route('/baby/<baby_id>/sleep/<sleep_id>/del', methods=['GET','POST'])
@login_required
def del_sleep(baby_id, sleep_id):
    print('in del')
    sleep= Sleep.query.filter_by(id=sleep_id).first()
    baby = Baby.query.filter_by(id=baby_id).first()
    db.session.delete(sleep)
    db.session.commit()
    return redirect(url_for('main_sleep', baby_id=baby.id))

@app.route('/baby/<baby_id>/sleep/<sleep_id>/end', methods=['GET','POST'])
@login_required
def end_sleep(baby_id, sleep_id):
    print('in end')
    sleep= Sleep.query.filter_by(id=sleep_id).first()
    baby = Baby.query.filter_by(id=baby_id).first()
    sleep.end_time=datetime.utcnow()
    sleep.sleep_duration=(sleep.end_time-sleep.start_time)
    db.session.commit()
    return redirect(url_for('main_sleep', baby_id=baby.id))

@app.route('/baby/<baby_id>/sleep', methods=['GET','POST'])
@login_required
def new_sleep(baby_id):
    form=SleepForm()
    baby=baby_id
    print('sleep create')
    sleep_type=form.sleep_type.data
    start_time=datetime.utcnow()
    sleep = Sleep(sleep_type=sleep_type,child_id=baby,start_time=start_time)
    db.session.add(sleep)
    db.session.commit()
    return render_template('/sleep.html', form=form)

