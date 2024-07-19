from flask import Blueprint, request
from app.controllers.user_controller import create_user as controller_create_user, get_user as controller_get_user


user = Blueprint('user', __name__)

@user.route('/', methods=['POST'])
def create_user():
    data = request.json
    user = data.get('email')
    password = data.get('pass')
    return controller_create_user(user, password)
@user.route('/check', methods=['GET'])
def get_user():
    return controller_get_user()
