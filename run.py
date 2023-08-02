from app import app, create_app
from flask_socketio import SocketIO

socketio = SocketIO(app)

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", )
