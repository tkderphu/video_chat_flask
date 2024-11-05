from flask import request, jsonify, Blueprint
from utils import utils
from service import messenger_service

messenger_bp = Blueprint('messenger', __name__, url_prefix="/api/v1/messenger")


@messenger_bp.route("/messages", methods=['POST'])
def createMessage():
    data = request.get_json();
    if utils.set_context_user_login(request) is None:
        return utils.exception_message
    return messenger_service.create_message(data);
@messenger_bp.route("/conversations",methods= ['GET'])
def getAllConversationOfCurrentUser():
    if utils.set_context_user_login(request) is None:
        return utils.exception_message;
    return jsonify(messenger_service.get_all_conversation_of_current_user());

@messenger_bp.route("/messages/conversations/<conversation_id>",methods= ['GET'])
def getAllMessageOfConversation(conversation_id):
    if utils.set_context_user_login(request) is None:
        return utils.exception_message;
    return jsonify(messenger_service.get_all_messages_of_conversation(conversation_id))

@messenger_bp.route("/conversations", methods=['POST'])
def createConversation():
    utils.set_context_user_login(request)
    return messenger_service.create_conversation(request.get_json());

@messenger_bp.route("/conversations/users/<user_id>", methods=['GET'])
def getPrivateConversation(user_id):
    return None

@messenger_bp.route("/conversations/{conversation_id/checkUser",methods= ['POST'])
def checkWhetherConversationContainsCurrentUser(conversation_id):
    return None