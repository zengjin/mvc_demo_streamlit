import os
from tinydb import TinyDB, Query

# 动态获取路径，确保在云端也能找到 db.json
db_path = os.path.join(os.path.dirname(__file__), '../../db.json')
db = TinyDB(db_path)
User = Query()

class UserModel:
    @staticmethod
    def get_all():
        return db.all()

    @staticmethod
    def add_user(username, role, name='', email='', password=''):
        if not db.search(User.username == username):
            db.insert({'username': username, 'role': role, 'name': name, 'email': email, 'password': password})
            return True
        return False

    @staticmethod
    def update_user(username, new_username=None, role=None, name=None, email=None, password=None):
        update_data = {}
        if new_username is not None:
            update_data['username'] = new_username
        if role is not None:
            update_data['role'] = role
        if name is not None:
            update_data['name'] = name
        if email is not None:
            update_data['email'] = email
        if password is not None:
            update_data['password'] = password
        db.update(update_data, User.username == username)
        return True

    @staticmethod
    def delete_user(username):
        db.remove(User.username == username)

    @staticmethod
    def get_user(username):
        return db.search(User.username == username)
