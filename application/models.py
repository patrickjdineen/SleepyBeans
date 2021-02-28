
from application import app, db
from datetime import datetime
import secrets

#Model for user table
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.column(db.String(100))
    last_name = db.column(db.String(100))
    email_address = db.Column(db.String(150))
    child = db.Relationship('Baby', backref = 'parent', lazy=True)

    def __init__(self,first_name,last_name,email_address):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address

#model for the baby table
class Baby(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.column(db.String(100))
    last_name = db.column(db.String(100))
    birth_date = db.Column(db.DateTime, nullable = False)
    gender = db.Colunm(db.String(50))
    parent_id = db.Column(db.String,db.ForeignKey('user.child'), nullable=False)
    sleep = db.Relationship('Sleep', backref="baby_id", lazy=True)

    def __init__(self,first_name,last_name,birth_date,gender,parent_id):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.parent_id = parent_id

#model for the sleep table
class Sleep(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    sleep_type = db.Column(db.String(150))
    start_time =  db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    sleep_duration = db.Column(db.DateTime)
    baby_id = db.Column(db.String, db.ForeignKey("baby.sleep"), nullable=False)

    def __init__(self,sleep_type,start_time,end_time,sleep_duration,baby_id):
        self.sleep_type = sleep_type
        self.start_time = start_time
        self.end_time = end_time
        self.sleep_duration = sleep_duration
        self.baby_id = baby_id