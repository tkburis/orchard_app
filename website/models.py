from . import db
from flask_login import UserMixin

class Tree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tree = db.Column(db.String(50), nullable=True)
    tree_type = db.Column(db.String(50), nullable=True)
    variety_name = db.Column(db.String(50), db.ForeignKey('variety.name'), nullable=True)
    variety = db.relationship('Variety', back_populates='trees', uselist=False)
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
    trees = db.relationship('Tree', back_populates='variety')
    name = db.Column(db.String(50), unique=True)
    scientific_name = db.Column(db.String(100), nullable=True)
    intro = db.Column(db.String(10000), nullable=True)
    origin = db.Column(db.String(100), nullable=True)
    history_and_description = db.Column(db.String(10000), nullable=True)
    characteristics = db.relationship('Characteristics', back_populates='variety', cascade='all, delete', uselist=False)
    characteristics_id = db.Column(db.Integer, db.ForeignKey('characteristics.id'))

class Characteristics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    variety = db.relationship('Variety', back_populates='characteristics')
    use = db.Column(db.String(100), nullable=True)
    colour = db.Column(db.String(100), nullable=True)
    flavour = db.Column(db.String(100), nullable=True)
    fruit_size = db.Column(db.String(100), nullable=True)
    picking_time = db.Column(db.String(100), nullable=True)
    season_of_use = db.Column(db.String(100), nullable=True)
    tree_vigour = db.Column(db.String(100), nullable=True)
    tree_habit = db.Column(db.String(100), nullable=True)
    fruit_bearing = db.Column(db.String(100), nullable=True)
    cropping = db.Column(db.String(100), nullable=True)
    disease_resistance = db.Column(db.String(100), nullable=True)
    suitable_for = db.Column(db.String(100), nullable=True)
    special_features = db.Column(db.String(100), nullable=True)
    pollination_date = db.Column(db.String(100), nullable=True)
    pollination_group = db.Column(db.String(100), nullable=True)
    self_fertility = db.Column(db.String(100), nullable=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
