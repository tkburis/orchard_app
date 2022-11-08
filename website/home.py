from flask import Blueprint, render_template, request
from flask_login import current_user
from .models import Tree
from .util import get_nearest_tree

home = Blueprint('home', __name__)

@home.route('/', methods=['GET', 'POST'])
def homepage():
    search_result = None
    if request.method == 'POST':
        user_lat = float(request.form.get('latitude'))
        user_long = float(request.form.get('longitude'))
        search_result = get_nearest_tree((user_lat, user_long))
    return render_template('home.html', search_result=search_result, current_user=current_user)

