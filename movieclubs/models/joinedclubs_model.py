from movieclubs.conf.mysqlconnection import connectToMySQL
from movieclubs.models import users_model

class Joined:
    
    def __init__(self, data):
        self.id = data['id']
        self.users_id = data['users_id']
        self.clubs_id = data['clubs_id']
        
    @classmethod
    def get_all(cls, data):
        query = """SELECT * FROM joined_clubs WHERE joined_clubs.clubs_id = %(id)s;"""
        results = connectToMySQL('movieclub').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])