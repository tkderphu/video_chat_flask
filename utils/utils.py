


auth_response_cache = {

}

expired_time = 86400000
exception_message = {
            "message": "You aren't login",
            "status": 400
        }
user_login = {
    'token': None
}
def set_context_user_login(request):
    if request.headers.get('Authorization'):
        token = str(request.headers.get('Authorization'))[5:];
        print(token)
        if auth_response_cache.get(token) is not None:
            user_login['id'] = auth_response_cache.get(token)['info']['id']
            user_login['fullName'] = auth_response_cache.get(token)['info']['fullName']
            return "ok"
    return None
