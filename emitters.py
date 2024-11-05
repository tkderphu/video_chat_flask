# emitters.py
from extensions.extensions import socketio

def send_response_message(data):
    socketio.emit('response', {'data': f'Message received: {data}'}, broadcast=True)
