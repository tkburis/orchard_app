from flask import Blueprint, render_template, abort
from flask_login import current_user
from .models import Variety

factfile_bp = Blueprint('factfile_bp', __name__)

@factfile_bp.route('/<int:variety_id>', methods=['GET', 'POST'])
def factfile(variety_id):
    variety_obj = Variety.query.filter_by(id=variety_id).first()
    if not variety_obj:
        abort(404)
    return render_template('factfile.html', variety=variety_obj)
