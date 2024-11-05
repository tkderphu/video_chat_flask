
from flask import jsonify, Blueprint, request
from service import user_service
from utils import utils
user_bp = Blueprint('user', __name__, url_prefix='/api/v1/users')

@user_bp.route('',methods=['GET'])
def get_users():
    if utils.set_context_user_login(request) is None:
        return utils.exception_message
    users = user_service.get_users()
    print(users)
    return jsonify(users);