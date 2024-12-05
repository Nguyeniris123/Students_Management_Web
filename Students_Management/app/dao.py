from app.models import User
from app import app
import hashlib

def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password)).first()

def get_user_by_id(id):
    return User.query.get(id)
