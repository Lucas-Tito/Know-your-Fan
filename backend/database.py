from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient('mongodb://mongodb:27017/')
        self.db = self.client['furia_fans']

    def save_user_data(self, user_data):
        return self.db.users.insert_one(user_data)

    def get_user_data(self, user_id):
        return self.db.users.find_one({'_id': user_id})

    def update_user_data(self, user_id, new_data):
        return self.db.users.update_one(
            {'_id': user_id},
            {'$set': new_data}
        )