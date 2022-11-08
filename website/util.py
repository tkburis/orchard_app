from .models import Tree
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
