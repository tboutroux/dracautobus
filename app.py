from routes import socketio, app
from flask_socketio import SocketIO

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)