from .models import Tree, Variety
from . import db
from geopy.distance import distance

def get_nearest_tree(user_coords):
    all_trees = Tree.query.all()
    if not all_trees:
        return None

    distances = {}

    for tree in all_trees:
        tree_coords = (tree.latitude, tree.longitude)
        dist = distance(user_coords, tree_coords).m
        distances[tree] = dist
    
    return min(distances, key=distances.get)

def get_or_create(model, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

def add_tree(**kwargs):
    if 'variety' in kwargs:
        variety_req = kwargs['variety']
        variety = get_or_create(Variety, name=variety_req)
        kwargs['variety_id'] = variety.id
    tree = Tree(**kwargs)
    db.session.add(tree)
    db.session.commit()
