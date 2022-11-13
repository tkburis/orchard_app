from . import db
from flask_login import UserMixin

class Tree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tree = db.Column(db.String(50), nullable=True)
    tree_type = db.Column(db.String(50), nullable=True)
    variety = db.Column(db.String(50), nullable=True)
    variety_id = db.Column(db.Integer, db.ForeignKey('variety.id'), nullable=True)
    root_stock = db.Column(db.String(50), nullable=True)
    flower_date = db.Column(db.String(50), nullable=True)
    pick_month = db.Column(db.String(50), nullable=True)
    planted = db.Column(db.String(50), nullable=True)
    position = db.Column(db.String(50), nullable=True)
    season_of_use = db.Column(db.String(50), nullable=True)
    dedication = db.Column(db.String(50), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

class Variety(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
