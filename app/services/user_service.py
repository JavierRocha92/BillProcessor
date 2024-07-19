
from ..db.Db import Db
import json
from ..models.User import User
def create_user(user : str, password : str) -> str:
    if not user_on_database(user):
        response = insert_user(User(user, password))
        return json.dumps(response)
    return json.dumps({'success': False, 'message': 'User has already been created'})

def insert_user(user):
    return Db().insert(user)

def user_on_database(user : str) -> bool:
    query = '''SELECT count() FROM users'''
    results = Db().run_query(query)
    results = [row[0] for row in results]
    return results[0] > 0

def get_user():
    query = '''SELECT * FROM users'''
    return Db().run_query(query)
