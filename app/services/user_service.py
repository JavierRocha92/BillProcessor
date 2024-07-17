
from app.db.Db import Db
from ..models.PDF_Extractor import PDF_Extractor as ext
import os
from ..models.Purchase import Purchase
from ..db.Db import Db
from ..functions.service_functions import get_error_message, get_unseen_emails
import json
from ..models.User import User
def create_user(user : str, password : str):
    if not user_on_database(user):
        response = insert_user(User(user, password))
        return json.dumps(response)
    return json.dumps({'success': False, 'message': 'User has already been created'})

def insert_user(user):
    return Db().insert(user)

def user_on_database(user : str):
    query = '''SELECT count() FROM users'''
    results = Db().run_query(query)
    results = [row[0] for row in results]
    return results[0] > 0

