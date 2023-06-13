from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blood_donor.db'  # Replace with your database URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager = LoginManager()

    db.init_app(app)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.donor import bp as donor_bp
    app.register_blueprint(donor_bp, url_prefix='/donor')

    return app
