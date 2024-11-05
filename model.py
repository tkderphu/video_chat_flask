from datetime import datetime

import utils.utils
from database import db

class Conversation(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=True)
    conversation_type = db.Column(db.String(150), default='PRIVATE')
    participants = db.relationship('Participation', backref='conversation', lazy=True)

    def __init__(self, name, conversation_type):
        self.name = name
        self.conversation_type = conversation_type

    def get_display(self):
        if self.conversation_type=='PRIVATE':
            if self.participants[0].user_id == utils.utils.user_login['id']:
                return self.participants[1].user.get_full_name()
            else:
                return self.participants[0].user.get_full_name()
        else:
            return self.name
    def to_dict_2(self, check):
        messages = Message.query.filter_by(conversation_id=self.id).all();
        res = {
            "id": self.id,
            'displayName': self.get_display(),
            'imageRepresent': None,
            'status': True,
            'scope': self.conversation_type,
        }
        if check is True:
            res['recentMessage'] = messages[len(messages) - 1].to_dict()
        return res;

    def to_dict(self):
        return self.to_dict_2(True)


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    message_type = db.Column(db.String(150))
    from_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, content, message_type, from_user_id, conversation_id):
        self.content = content
        self.message_type = message_type
        self.from_user_id = from_user_id
        self.conversation_id = conversation_id

    def to_dict(self):
        user: User = User.query.filter_by(id=self.from_user_id).first()
        conversation: Conversation = Conversation.query.filter_by(id=self.conversation_id).first()
        return {
            'id': self.id,
            'content': self.content,
            'messageType': self.message_type,
            'fromUser': user.to_dict(),
            'toConversation': conversation.to_dict_2(False),
            'createdDate': self.created_date.strftime('%Y-%m-%d %H:%M:%S'),
        }


class Participation(db.Model):
    __tablename__ = 'participations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"), nullable=False)

    def __init__(self, user_id, conversation_id):
        self.user_id = user_id
        self.conversation_id = conversation_id


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    online = db.Column(db.Boolean, nullable=False, default=False)
    participants = db.relationship('Participation', backref='user', lazy=True)

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def to_dict(self):
        return {
            "id": self.id,
            'fullName': self.get_full_name(),
            'online': self.online
        }
