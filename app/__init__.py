import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'routes.login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)

    # Konfiguracija
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-dev-key-change-me')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicijalizacija ekstenzija sa aplikacijom
    db.init_app(app)
    login_manager.init_app(app)

    # Registracija ruta (Blueprint)
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # Kreiranje baze ako ne postoji
    with app.app_context():
        db.create_all()

    return app