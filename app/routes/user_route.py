from flask import Blueprint, request
from app.controllers.user_controller import create_user as controller_create_user


user = Blueprint('user', __name__)

@user.route('/', methods=['POST'])
def create_user():
    data = request.json
    user = data.get('user')
    password = data.get('pass')
    return controller_create_user(user, password)
