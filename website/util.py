from .models import Tree, Variety, Characteristics
from . import db
from geopy.distance import distance

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
        variety_req = kwargs['variety_name']
        add_variety(variety_req)
    tree = Tree(**kwargs)
    db.session.add(tree)
    db.session.commit()
