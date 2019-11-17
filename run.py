from backend import app
from backend import socketio

if __name__ == '__main__':
    app.debug = True
    socketio.run(app, port=5000, debug=True)