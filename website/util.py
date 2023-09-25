from .models import Tree, Variety, Characteristics
from . import db
from geopy.distance import distance

TREE_KEY_NAMES = {
    'tree': 'Tree',
    'tree_type': 'Tree type',
    'variety_name': 'Variety name',
    'root_stock': 'Root stock',
    'flower_date': 'Flower date',
    'pick_month': 'Pick month',
    'planted': 'Planted',
    'position': 'Position',
    'season_of_use': 'Season of use',
    'dedication': 'Dedication',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
}

CHAR_KEY_NAMES = {
    'name': 'Name',
    'scientific_name': 'Scientific name',
    'intro': 'Introduction',
    'origin': 'Origin',
    'description': 'Description',
    'use': 'Use',
    'colour': 'Colour',
    'flavour': 'Flavour',
    'fruit_size': 'Fruit size',
    'picking_time': 'Picking time',
    'season_of_use': 'Season of use',
    'tree_vigour': 'Tree vigour',
    'tree_habit': 'Tree habit',
    'fruit_bearing': 'Fruit bearing',
    'cropping': 'Cropping',
    'disease_resistance': 'Disease resistance',
    'suitable_for': 'Suitable for',
    'special_features': 'Special features',
    'pollination_date': 'Pollination date',
    'pollination_group': 'Pollination group',
    'self_fertility': 'Self fertility',
}

def get_nearest_tree(user_coords):
    all_trees = Tree.query.all()
    if not all_trees or all([(tree.latitude, tree.longitude) == (None, None) for tree in all_trees]):
        return None

    distances = {}

    for tree in all_trees:
        tree_coords = (tree.latitude, tree.longitude)
        dist = distance(user_coords, tree_coords).m
        distances[tree] = dist
    
    return min(distances, key=distances.get)

# adds new variety if does not exist already
def add_variety(name):
    instance = Variety.query.filter_by(name=name).first()
    if not instance:
        char = Characteristics()
        instance = Variety(name=name, characteristics=char)
        db.session.add(instance)
        db.session.commit()

def add_tree(**kwargs):
    if 'variety_name' in kwargs:
        variety_name = kwargs['variety_name']
        if variety_name:
            add_variety(variety_name)
    tree = Tree(**kwargs)
    db.session.add(tree)
    db.session.commit()
