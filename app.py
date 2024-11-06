from flask import Flask
from extensions.extensions import socketio
from flask_cors import CORS
from database import db
from blueprints.auth_blueprint import auth_bp
from blueprints.user_blueprint import user_bp
from blueprints.messenger_blueprint import messenger_bp
from emitters import send_response_message  #
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/video_chat_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
CORS(app)  # Allow only frontend's origin
socketio.init_app(app, cors_allowed_origins="http://localhost:4200")
db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(messenger_bp)

# Ensure tables are created
with app.app_context():
    db.create_all()

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    socketio.emit('response', {'data': 'Connected to WebSocket server!'})

@socketio.on('message')
def handle_message(msg):
    print(f"Received message: {msg}")
    socketio.emit('test', {'data': f'Message received: {msg}'})

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")


@app.route('/emit_message/<msg>')
def emit_message(msg):
    send_response_message(msg)  # Call the function to emit message
    return {'status': 'Message emitted'}

@socketio.on('/topic/private')
def test(msg):
    print(f"Custom message: {msg}")

@socketio.on('/signal')
def establish_video(signal):
    socketio.emit('/topic/room', signal)

if __name__ == '__main__':
    socketio.run(app, host="localhost", port=8080, debug=True)
