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
    def add_user(username, role):
        if not db.search(User.username == username):
            db.insert({'username': username, 'role': role})
            return True
        return False

    @staticmethod
    def delete_user(username):
        db.remove(User.username == username)
