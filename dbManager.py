from connection import my_db

class dbManager:
    def __init__(self):
        self.comment_collection = my_db['comments']
        self.user_collection = my_db['users']

    def addComment(self, datas):
        self.comment_collection.insert_many(datas)
    
    
    def importComment(self, user_name, my_key, my_value):
        result = self.comment_collection.find({'$and': [{'user': {'$eq': user_name}}, {my_key: {'$eq': my_value}}]}, {'_id': 0})

        return result


    def addUser(self, user):
        self.user_collection.insert_one(user)
    
    def loginControl(self, user_name, user_password):
        result = self.user_collection.find_one({'$and':[{'name': {'$eq': user_name}}, {'password': {'$eq': user_password}}]})
        if result:
            return result
        else:
            return None
    
    def registerControl(self, user_name):
        result = self.user_collection.find_one({'name': {'$eq': user_name}})

        if result:
            return result
        else:
            return None
