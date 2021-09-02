# __init__.py makes the folder a complete py package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initializing SQLAlchemy  
db = SQLAlchemy()
DB_NAME = "database.db"

# Defininining app func.
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'This secret key can be anything you want'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Importing these variables from their corresponding files
    from .views import views
    from .auth import auth

    # Registering views % auth blueprints in the app 
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')


    from .models import User,Note

    # Creating database for the app
    create_database(app)

    login_manager = LoginManager()
    # Where we want to redirect user if login is req. and user not logged in
    login_manager.login_view = 'auth.login'
    # Telling login manager which app we're refering to
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Will create DB if it's not alredy created.
def create_database(app):
    if not path.exists('website/'+DB_NAME):
        db.create_all(app=app)
        print('Created Database!')