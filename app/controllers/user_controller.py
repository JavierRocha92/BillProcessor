import json

from app.services.user_service import create_user as service_create_user
def create_user(user : str, password : str):
    return service_create_user(user, password)


