from .database import db
from flask_security import RoleMixin, UserMixin

roles_users = db.Table('roles_users',
 db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
 db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    trackers = db.relationship("Tracker", backref="tracker")
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))            

class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Tracker(db.Model):
    __tablename__ = "tracker"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    type = db.Column(db.Integer, nullable=False)
    settings = db.Column(db.String)
    user_id = db.Column(db.Integer,  db.ForeignKey("user.id"), nullable=False)
    activity = db.relationship("Activity", backref="activity")

class Activity(db.Model):
    __tablename__ = "activity"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.String, nullable=False)
    note = db.Column(db.String, nullable=False)
    tracker_id = db.Column(db.Integer, db.ForeignKey("tracker.id"), nullable=False)
