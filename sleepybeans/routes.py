from sleepybeans import app, db, login_manager
from flask import render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, current_user, login_required

from sleepybeans.models import User, Baby, Sleep, check_password_hash
from sleepybeans.forms import UserLoginForm, DateField, UserSignUpForm, BabyForm

#TBD
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)

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
    babies = babies)
    # first_name = user.first_name,
    # baby_name=baby.name,
    # baby_birthdate=baby.birth_date)

#Page to create baby and commit them to DB
@app.route('/baby', methods= ['GET','POST'])
@login_required
def baby():
    form = BabyForm()
    if request.method == 'POST':
        names = form.name.data
        date=form.birthdate.data
        new_baby = Baby(name=names, birth_date=date, parent_id=current_user.token)
        db.session.add(new_baby)
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        print("fail")
    return render_template('/baby.html',form=form)

#Sleep Tracking page
@app.route('/sleep', methods= ['GET','POST'])
def sleep():
    if request.form:
        print(request.form)
    return render_template('/sleep.html')