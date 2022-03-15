from .database import db

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False)
    hashkey = db.Column(db.String, nullable=False)


class Tracker(db.Model):
    __tablename__ = "tracker"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    type = db.Column(db.Integer, nullable=False)
    settings = db.Column(db.String)
    user_id = db.Column(db.Integer, nullable=False)
    activity = db.relationship("Activity", backref="activity")

class Activity(db.Model):
    __tablename__ = "activity"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.String, nullable=False)
    note = db.Column(db.String, nullable=False)
    tracker_id = db.Column(db.Integer, db.ForeignKey("tracker.id"), nullable=False)
