from flask import Blueprint, render_template, request
from flask_login import current_user
from .models import Tree, Variety
from .util import get_nearest_tree

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/', methods=['GET', 'POST'])
def home():
    search_result = None
    keys = Tree.__table__.columns.keys()
    all_varieties = Variety.query.all()
    if request.method == 'POST':
        user_lat = float(request.form.get('latitude'))
        user_long = float(request.form.get('longitude'))
        search_result = get_nearest_tree((user_lat, user_long))
    return render_template('home.html',
                            search_result=search_result,
                            keys=keys,
                            all_varieties=all_varieties)

