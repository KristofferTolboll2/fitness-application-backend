from backend import app
from backend import socket

if __name__ == '__main__':
    app.debug = True
    socket.run(app, port=5000, debug=True, use_reloader=True)