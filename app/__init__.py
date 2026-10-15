import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
login_manager.login_view = 'routes.login'
login_manager.login_message = 'Prijavi se da bi video ovu stranicu.'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'samo-za-lokalni-rad')
    # Neon i Render daju link oblika postgresql://..., a aplikacija koristi
    # psycopg2 drajver, pa se on navodi izričito.
    db_url = os.environ.get('DATABASE_URL') or 'sqlite:///blog.db'
    for prefix in ('postgres://', 'postgresql://'):
        if db_url.startswith(prefix):
            db_url = 'postgresql+psycopg2://' + db_url[len(prefix):]
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    # CSRF zaštita i za forme koje nisu FlaskForm (npr. brisanje članka)
    csrf.init_app(app)

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    from app.prose import render_prose
    app.add_template_filter(render_prose, 'prose')

    with app.app_context():
        db.create_all()

        # Primeri članaka za prazan blog (SEED_DEMO_POSTS=true na serveru)
        if os.environ.get('SEED_DEMO_POSTS') == 'true':
            from app.seed import seed_demo_posts
            seed_demo_posts()

    return app