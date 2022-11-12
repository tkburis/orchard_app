from . import db
from flask_login import UserMixin

class Tree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tree = db.Column(db.String(50))
    tree_type = db.Column(db.String(50))
    variety = db.Column(db.String(50))
    root_stock = db.Column(db.String(50))
    flower_date = db.Column(db.String(50))
    pick_month = db.Column(db.String(50))
    planted = db.Column(db.String(50))
    position = db.Column(db.String(50))
    season_of_use = db.Column(db.String(50))
    dedication = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
