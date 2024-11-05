from flask import request, jsonify, Blueprint
from service import auth_service
auth_bp = Blueprint('auth', __name__, url_prefix="/api/v1/users/auth")


# from utils import utils
@auth_bp.route('/login', methods=['POST'])
def login():
    loginRequest = request.get_json()
    # response = authen_service.authenticate(loginRequest);
    return jsonify(auth_service.authenticate(loginRequest))

@auth_bp.route('/register', methods=['POST'])
def register():
    register_request = request.get_json();
    return jsonify(auth_service.register(register_request))

