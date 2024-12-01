from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from pydantic import BaseModel, constr, Field

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    usernum = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    firstname = db.Column(db.String(80), nullable=True)
    lastname = db.Column(db.String(80), nullable=True)
    team = db.Column(db.String(80), nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    completion_rate = db.Column(db.Float, nullable=True)
    total_points = db.Column(db.Integer, nullable=True)
    peer_ratings = db.Column(db.JSON, nullable=True)
    peer_rate = db.Column(db.Float, nullable=True)
    performance = db.Column(db.JSON, nullable=True)
    sprint_pts = db.Column(db.JSON, nullable=True)
    time = db.Column(db.JSON, nullable=True)
    tasks = db.relationship('Task', backref='user', lazy=True)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    tasknum = db.Column(db.Integer, unique=True, nullable=False)
    sprint = db.Column(db.Integer, nullable=False)
    time_assigned = db.Column(db.DateTime, nullable=False)
    status_completed = db.Column(db.Boolean, nullable=False)
    time_completed = db.Column(db.DateTime, nullable=True)
    point = db.Column(db.Integer, nullable=False)
    usernum = db.Column(db.Integer, db.ForeignKey('users.usernum'), nullable=False)

class RegisterModel(BaseModel):
    username: constr(min_length=1)
    password: constr(min_length=1)
    cf_password: constr(min_length=1)
    first_name: constr(min_length=1)
    last_name: constr(min_length=1)
    team: constr(min_length=1)

class LoginModel(BaseModel):
    username: constr(min_length=1)
    password: constr(min_length=1)

class ChangePasswordModel(BaseModel):
    old_password: constr(min_length=1)
    new_password: constr(min_length=1)
    cf_password: constr(min_length=1)

class RegisterModel(BaseModel):
    username: constr(min_length=1)
    password: constr(min_length=1)
    cf_password: constr(min_length=1)
    first_name: constr(min_length=1)
    last_name: constr(min_length=1)
    team: constr(min_length=1)

class LoginModel(BaseModel):
    username: constr(min_length=1)
    password: constr(min_length=1)

class ChangePasswordModel(BaseModel):
    old_password: constr(min_length=1)
    new_password: constr(min_length=1)
    cf_password: constr(min_length=1)