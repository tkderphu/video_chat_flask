from database import  db
from model import  Conversation
from model import  Message
from model import  Participation
from utils import utils
from response.api_response import APIResponse
from extensions.extensions import socketio
def create_message(message_request):
    conversation = Conversation.query.filter_by(id=message_request['destId']).first()
    # content, message_type, from_user_id, conversation_id
    if conversation is None:
        conversation = Conversation(
            None,
            'PRIVATE'
        )
        db.session.add(conversation)
        db.session.commit()
        participation = Participation(
            user_id=message_request['destId'],
            conversation_id=conversation.id
        )
        db.session.add(participation)
        participation = Participation(
            user_id=utils.user_login.get('id'),
            conversation_id=conversation.id
        )
        db.session.add(participation)
        db.session.commit()

    if message_request['video'] is True:
        type = 'VIDEO'
    else:
        type = 'TEXT'
    message = Message(
        message_request['content'],
        type,
        utils.user_login['id'],
        conversation.id
    )
    db.session.add(message)
    db.session.commit()


    for participation in conversation.participants:
        print("hello world: user - ", participation.user_id)
        topic = f'/topic/private/messages/conversation/user/{participation.user_id}'
     ##"/topic/private/conversation/user/" + str(participation.user_id)
        socketio.emit(topic, message.to_dict())
        # socketio.emit('response', {'data': f'Message received: {'data'}'}, namespace='/')
    return APIResponse('', 200, 0, message.to_dict()).to_dict();
def create_conversation(conversation_request):
    conversation = Conversation(conversation_request['name'], 'PUBLIC')
    db.session.add(conversation)
    db.session.commit()
    for userId in conversation_request['userIds']:
        participation = Participation(
            user_id=userId,
           conversation_id= conversation.id
        )
        db.session.add(participation)
    message = Message(f'----->User {utils.user_login.get("fullName")} created group <-----',
                      'TEXT',
                      utils.user_login.get('id'),
                      conversation.id)
    db.session.add(message)
    db.session.commit()

    for id in conversation_request['userIds']:
        socketio.emit("/topic/private/conversation/user/" + str(id), conversation.to_dict(), broadcast=True)

    return APIResponse('', 200, 0, conversation.to_dict_2(False)).to_dict();

def get_all_conversation_of_current_user():
    conversations = []
    participations = Participation.query.all()
    for participation in participations:
        if participation.user.id == utils.user_login.get('id'):
            conversations.append(participation.conversation.to_dict())
    return APIResponse('', 200, 0, conversations).to_dict();

def get_all_messages_of_conversation(conversation_id):
    message = Message.query.filter_by(conversation_id=conversation_id).all()
    msg = []
    for m in message:
        msg.append(m.to_dict())
    return APIResponse('', 200, 0, msg).to_dict()


def findPrivateConversation(user_id):
    conversations = Conversation.query.filter_by(conversation_type='PRIVATE')
    res = None
    for conversation in conversations:
        if (conversation.participants[0].user_id + conversation.participants[1].user_id)  == int( user_id )+ int(utils.user_login.get('id')):
            res = conversation
            break
    if res == None:
        return APIResponse(None, 400, 0, {}).to_dict();
    else:
        return APIResponse(None, 200, 0, res.to_dict()).to_dict();
def checkConversationContainsCurrentUser(conversation_id):
    participations = Participation.query.filter_by(conversation_id=conversation_id).all();
    api = APIResponse('', 200, 0, False)
    for participation in participations:
        if participation.user.id == utils.user_login.get('id'):
            api.data = True
            break
    return api.to_dict()