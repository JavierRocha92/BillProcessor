import json

from app.services.user_service import create_user as service_create_user, get_user as service_get_user
def create_user(user : str, password : str):
    return service_create_user(user, password)
def get_user():
    results = service_get_user()
    if len(results):
        return json.dumps({'success': True, 'message' : results[0][1]})
    return json.dumps({'success' : False, 'message' : 'User is not on database'})
