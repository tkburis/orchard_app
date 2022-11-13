from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from os.path import join, dirname, abspath, exists
from os import environ

db = SQLAlchemy()
DB_NAME = environ.get('DB_NAME')

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{DB_NAME}'
    )

    db.init_app(app)
    create_database(app)

    from .home import home_bp
    from .admin import admin_bp

    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/admin/')

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'admin_bp.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    from .models import Tree, User
    db_path = join(dirname(dirname(abspath(__file__))), 'instance', DB_NAME)
    if not exists(db_path):
        with app.app_context():
            db.create_all()
            print('Database created')

            # TODO: delete this
            from .util import add_tree
            add_tree(tree='Apple',
                        tree_type='Eat',
                        variety='Adams Pearmain',
                        root_stock='M25',
                        flower_date=9,
                        pick_month='October',
                        planted='February 2009',
                        position='14',
                        season_of_use='November - March',
                        dedication='Marcus Scaramanga',
                        latitude=51.20450568383156,
                        longitude=0.27311582088819875)
            add_tree(variety='Some other variety')
            add_tree(variety='Adams Pearmain')
            add_tree(variety='Some other variety')

            admin_user = User(username='admin', password=generate_password_hash(environ.get('ADMIN_PW')))
            db.session.add(admin_user)
            db.session.commit()
            