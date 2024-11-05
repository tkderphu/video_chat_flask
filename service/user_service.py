import utils.utils
from model import User
from response.api_response import APIResponse
def get_users():
    users = []
    for user in User.query.all():
        if user.id != utils.utils.user_login['id']:
            users.append(user.to_dict())
    return APIResponse(
        "get users",
        200,
        0,
        users).to_dict();