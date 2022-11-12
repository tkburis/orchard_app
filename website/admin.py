from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import json
from .models import Tree, User
from . import db

admin = Blueprint('admin', __name__)

@admin.route('/', methods=['GET', 'POST'])
@login_required
def admin_page():
    keys = Tree.__table__.columns.keys()
    if request.method == 'POST':
        form_data = {key: request.form.get(key) for key in keys}
        
        new_tree = Tree(**form_data)
        
        db.session.add(new_tree)
        db.session.commit()
        flash('Tree added', category='success')

    all_trees = Tree.query.all()
    return render_template('admin.html',
                            all_trees=all_trees,
                            keys=keys,
                            current_user=current_user)

@admin.route('/delete-tree', methods=['POST'])
def delete_tree():
    tree_req = json.loads(request.data)
    tree_id = tree_req['treeId']
    tree = Tree.query.get(tree_id)
    if tree:
        db.session.delete(tree)
        db.session.commit()
    flash('Tree deleted', category='success')
    return jsonify({})

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('admin.admin_page'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Username does not exist', category='error')

    return render_template('login.html', current_user=current_user)

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', category='success')
    return redirect(url_for('home.homepage'))
