from flask import Flask
from blood_donor_app2.blood_donor_app.app.database import db
from blood_donor_app2.blood_donor_app.app.routes import bp as main_bp
from blood_donor_app2.blood_donor_app.app.admin import bp as admin_bp
from blood_donor_app2.blood_donor_app.app.donor import bp as donor_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blood_donor.db'  # Replace with your database URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(main_bp)

    app.register_blueprint(admin_bp, url_prefix='/admin')

    app.register_blueprint(donor_bp, url_prefix='/donor')

    return app
