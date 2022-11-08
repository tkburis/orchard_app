from . import db
from flask_login import UserMixin

class Tree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year_planted = db.Column(db.Integer)
    species = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
