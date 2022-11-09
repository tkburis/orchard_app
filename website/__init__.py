from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from os.path import join, dirname, abspath, exists
from os import path, environ

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

    from .home import home
    from .admin import admin

    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin/')

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'admin.login'
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
            # tree1 = Tree(year_planted=2006,
            #             species='Species #1',
            #             latitude=51.20450568383156,
            #             longitude=0.27311582088819875)
            # db.session.add(tree1)
            # tree2 = Tree(year_planted=2004,
            #             species='Species #2',
            #             latitude=51.204535513015905,
            #             longitude=0.27316745341299326)
            # db.session.add(tree2)
            # tree3 = Tree(year_planted=2015,
            #             species='Species #3',
            #             latitude=51.20457626553227,
            #             longitude=0.2731037509473378)
            # db.session.add(tree3)

            admin_user = User(username='admin', password=generate_password_hash(environ.get('ADMIN_PW')))
            db.session.add(admin_user)
            db.session.commit()