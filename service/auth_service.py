import time
import uuid
from database import db
from model import User
from utils.utils import *
from response.api_response import APIResponse
def authenticate(login_request: dict):
    if(login_request is None):
        return APIResponse(
        "can't null",
        400,
        1,
        None).to_dict();
    user : User = User.query.filter_by(email=login_request['email']).first();
    if(user and user.password == login_request['password']):
        auth_response = {
            'uuid': str(uuid.uuid4()),
            'expiredTime': int(round(time.time() * 1000)) + expired_time,
            'info': {
                'fullName': user.first_name + " " + user.last_name,
                'id': user.id
            }
        }
        auth_response_cache[auth_response['uuid']] = auth_response
        return APIResponse('', 200, 0, auth_response).to_dict();
    return APIResponse(
        "Username or password not match",
        400,
        1,
        None
    ).to_dict()
def register(register_request):
    if (register_request is None):
        APIResponse(
            "Request can't null",
            400,
            1,
            None
        ).to_dict()
    user = User(
        register_request['email'],
        register_request['password'],
        register_request['firstName'],
        register_request['lastName']
    )
    db.session.add(user)
    db.session.commit()
    return APIResponse(
        "Created account successfully",
        200,
        0,
        None
    ).to_dict()

