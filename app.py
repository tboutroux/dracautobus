from routes import socketio, app
from flask_socketio import SocketIO

if __name__ == '__main__':
    socketio.run(app, debug=True)