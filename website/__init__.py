from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import os

load_dotenv()
db = SQLAlchemy()
DB_NAME = os.environ.get('DB_NAME')

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{DB_NAME}',
        UPLOAD_FOLDER=os.path.join(app.instance_path, os.environ.get('UPLOAD_FOLDER')),
    )

    db.init_app(app)
    create_database(app)

    from .home import home_bp
    from .admin import admin_bp
    from .factfile import factfile_bp
    from .api import api_bp

    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/admin/')
    app.register_blueprint(factfile_bp, url_prefix='/factfile/')
    app.register_blueprint(api_bp, url_prefix='/api/')
    
    from .errors import page_not_found
    
    app.register_error_handler(404, page_not_found)

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'admin_bp.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    return app

def create_database(app):
    from .models import Tree, User, Variety, Characteristics
    db_path = os.path.join(app.instance_path, DB_NAME)
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            print('Database created')

            # TODO: delete this
            # from .util import add_tree
            # add_tree(tree='Apple',
            #             tree_type='Eat',
            #             variety_name='Adams Pearmain',
            #             root_stock='M25',
            #             flower_date=9,
            #             pick_month='October',
            #             planted='February 2009',
            #             position='14',
            #             season_of_use='November - March',
            #             dedication='Marcus Scaramanga',
            #             latitude=51.20450568383156,
            #             longitude=0.27311582088819875)
            # add_tree(variety_name='Some other variety')
            # add_tree(variety_name='Adams Pearmain')
            # add_tree(variety_name='Some other variety')
            
            admin_user = User(username='admin', password=generate_password_hash(os.environ.get('ADMIN_PW')))
            db.session.add(admin_user)
            db.session.commit()
            
            # TODO: delete this
            # v = Variety.query.filter_by(name='Adams Pearmain').first()
            # v.characteristics.use = 'Dessert'
            