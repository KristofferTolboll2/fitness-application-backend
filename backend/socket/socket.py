from backend import socket

@socket.on('connect')
def on_connect():
    print('User connected')

@socket.on('send_message')
def on_send_message(data):
    print(f'data received was {data}')
