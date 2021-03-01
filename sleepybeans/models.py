
from application import app, db, login_manager
from datetime import datetime, timedelta, date
import secrets
import uuid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#Model for user table
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(100), nullable = True)
    last_name = db.Column(db.String(100), nullable = True)
    email_address = db.Column(db.String(150))
    password = db.Column(db.String, nullable = True)
    token = db.Column(db.String, unique=True)
    child = db.relationship('Baby', backref = 'parent', lazy=True)

    def __init__(self,first_name,last_name,email_address,password,token):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.password = set_password(password)
        self.token = set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4)

    def set_password(self, password):
        self.pw_hash=generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"{self.first_name} {self.last_name} has been added to the User Table"

#model for the baby table
class Baby(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    birth_date = db.Column(db.DateTime, nullable = False)
    parent_id = db.Column(db.String,db.ForeignKey('user.token'), nullable=False)
    sleep = db.relationship('Sleep', backref= "baby", lazy=True)

    def __init__(self,name,birth_date,,parent_id):
        self.id = set_id()
        self.name = name
        self.birth_date = birth_date
        self.parent_id = parent_id

    def set_id(self):
        return str(uuid.uuid4)

    def __repr__(self):
        return f"{self.first_name} has been added to the Baby Table"

#model for the sleep table
class Sleep(db.Model):
    id = db.Column(db.String, primary_key =True)
    sleep_type = db.Column(db.String(150))
    start_time =  db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    sleep_duration = db.Column(db.DateTime)
    child_id = db.Column(db.String, db.ForeignKey("baby.id"), nullable=False)

    def __init__(self,sleep_type,start_time,end_time,sleep_duration,baby_id):
        self.id = set_id()
        self.sleep_type = sleep_type
        self.start_time = start_time
        self.end_time = end_time
        self.sleep_duration = sleep_duration
        self.child_id = child_id

    def set_id(self):
        return str(uuid.uuid4)

    def __repr__(self):
        return f"Sleep starting at {self.start_time} has been added to the sleep table"