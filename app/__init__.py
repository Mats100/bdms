from flask_socketio import SocketIO
from app.database import db
from app.models import Donor, Admin
from app.routes import bp as main_bp
from app.admin import bp as admin_bp
from app.donor import bp as donor_bp
from flask import Flask
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blood_donor.db'  # Replace with your database URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'donor.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        donor = Donor.query.get(int(user_id))
        if donor:
            return donor

        admin = Admin.query.get(int(user_id))
        if admin:
            return admin

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(donor_bp, url_prefix='/donor')

    return app


app = create_app()
socketio = SocketIO(app)


if __name__ == '__main__':
    socketio.run(app.run(debug=True, host="0.0.0.0"), allow_unsafe_werkzeug=True)

