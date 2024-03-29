from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user, current_user
import json
import os

from .models import Tree, User, Variety, Characteristics
from . import db
from .util import add_tree, add_variety, TREE_KEY_NAMES, CHAR_KEY_NAMES

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/trees', methods=['GET', 'POST'])
@login_required
def trees():
    keys = Tree.__table__.columns.keys()
    
    if request.method == 'POST':
        form_data = request.form.to_dict()
        for k in form_data:
            if not form_data[k]:
                form_data[k] = None
        form_type = form_data.pop('type')
        
        if form_type == 'edit':
            tree_id = form_data.pop('id')
            tree_obj = Tree.query.get(tree_id)
            
            for k, v in form_data.items():
                print(v)
                if k == 'variety_name' and v:
                    print("ADDED", v)
                    add_variety(v)
                setattr(tree_obj, k, v)
            db.session.commit()
            flash('Tree edited', category='success')
            
        else:  # add
            print(form_data['variety_name'])
            add_tree(**form_data)
            flash('Tree added', category='success')

    all_trees = Tree.query.all()
    return render_template('trees.html',
                            all_trees=all_trees,
                            keys=keys,
                            TREE_KEY_NAMES=TREE_KEY_NAMES)

@admin_bp.route('/delete-tree', methods=['POST'])
@login_required
def delete_tree():
    tree_req = json.loads(request.data)
    tree_id = tree_req['treeId']
    tree = Tree.query.get(tree_id)
    if tree:
        db.session.delete(tree)
        db.session.commit()
    flash('Tree deleted', category='success')
    return jsonify({})

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ('png', 'jpg', 'jpeg')

@admin_bp.route('/varieties', methods=['GET', 'POST'])
@login_required
def varieties():
    all_varieties = Variety.query.all()
    variety_keys = Variety.__table__.columns.keys()
    char_keys = Characteristics.__table__.columns.keys()
    
    if request.method == 'POST':
        form_data = request.form.to_dict()

        for k in form_data:
            if not form_data[k]:
                form_data[k] = None

        variety_id = form_data.pop('id')
        variety_data = {}
        char_data = {}
        
        for k, v in form_data.items():
            if k.startswith('char_'):
                char_data[k.removeprefix('char_')] = v
            else:
                variety_data[k] = v
                
        variety_obj = Variety.query.get(variety_id)
        for k, v in variety_data.items():
            setattr(variety_obj, k, v)
        for k, v in char_data.items():
            setattr(variety_obj.characteristics, k, v)
        
        if 'picture' in request.files:
            picture = request.files['picture']
            print(picture)
            if picture and allowed_file(picture.filename): 
                filename = secure_filename(picture.filename)
                extension = filename.rsplit('.', 1)[1].lower()
                picture.save(os.path.join(current_app.config['UPLOAD_FOLDER'], f'{variety_id}.{extension}'))
                variety_obj.picture_filename = f'{variety_id}.{extension}'
            elif picture.filename != '':  # don't flash error if no file was selected
                flash('Invalid file', 'error')
        
        db.session.commit()

        flash('Variety edited', category='success')
        
    return render_template('varieties.html',
                           all_varieties=all_varieties,
                           variety_keys=variety_keys,
                           char_keys=char_keys,
                           CHAR_KEY_NAMES=CHAR_KEY_NAMES)

@admin_bp.route('/delete-variety', methods=['POST'])
@login_required
def delete_variety():
    variety_req = json.loads(request.data)
    variety_id = variety_req['varietyId']
    variety_obj = Variety.query.get(variety_id)
    if variety_obj:
        if len(variety_obj.trees) > 0:
            flash('There are still trees with this variety - delete them first', category='error')
        else:
            db.session.delete(variety_obj)
            db.session.commit()
            flash('Variety deleted', category='success')
    return jsonify({})

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('admin_bp.trees'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Username does not exist', category='error')

    return render_template('login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', category='success')
    return redirect(url_for('home_bp.home'))
