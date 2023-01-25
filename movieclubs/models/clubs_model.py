from movieclubs.conf.mysqlconnection import connectToMySQL
from movieclubs.models import users_model
from flask import flash

class Club:
    
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.genre = data['genre']
        self.description =  data['description']
        
    @classmethod
    def createclub(cls, data):
        query =  """INSERT INTO clubs (name, genre, description, users_id)
                    VALUES (%(name)s, %(genre)s, %(description)s, %(users_id)s);"""
        return connectToMySQL('movieclub').query_db(query, data)
    
    @classmethod
    def insertpost(cls, data):
        query = """UPDATE clubs
                    SET posts_id = %(posts.id)s
                    WHERE id = %(id)s"""
        return connectToMySQL('movieclub').query_db(query, data)
    
    @classmethod
    def updateclub(cls, data):
        query = """UPDATE clubs
                    SET name = %(name)s, genre = %(genre)s, description = %(description)s
                    WHERE id = %(id)s;"""
        return connectToMySQL('movieclub').query_db(query, data)
    
    @classmethod
    def get_all_clubs(cls):
        query = """SELECT * FROM clubs;"""
        results = connectToMySQL('movieclub').query_db(query)
        clubs = []
        for club in results:
            clubs.append(cls(club))
        return clubs
    
    @classmethod
    def leave_club(cls, data):
        query = """DELETE FROM joined_clubs WHERE clubs_id = %(id)s"""
        return connectToMySQL('movieclub').query_db(query, data);
    
    
    @classmethod
    def get_created_club(cls, data):
        query = """SELECT * FROM clubs WHERE id = %(id)s;"""
        results = connectToMySQL('movieclub').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def unjoined_clubs(cls,data):
        query = "SELECT * FROM clubs WHERE clubs.id NOT IN ( SELECT clubs_id FROM joined_clubs WHERE users_id = %(id)s );"
        results = connectToMySQL('movieclub').query_db(query,data)
        clubs = []
        for row in results:
            clubs.append(cls(row))
        print(clubs)
        return clubs
    
    @classmethod
    def get_users_club(cls, data):
        query = """SELECT * FROM clubs JOIN users ON clubs.users_id = users.id
                    WHERE clubs.id = %(id)s;"""
        results = connectToMySQL('movieclub').query_db(query, data)
        clubs = []
        for club in results:
            one_club = cls(club)
            user = {"id" : club["users.id"],
                    'first_name': club['first_name'],
                    'last_name' : club['last_name'],
                    'email': club['email'],
                    'username' : club['username'],
                    'fav_genre1' : club['fav_genre1'],
                    'fav_genre2' : club['fav_genre2'],
                    'fav_genre3' : club['fav_genre3'],
                    'bio' : club['bio'],
                    'password' : None}
            one_club.clubber = users_model.User(user)
            clubs.append( one_club )
        return clubs
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM clubs WHERE clubs.id = %(id)s;"
        return connectToMySQL('movieclub').query_db(query, data)
    
    @staticmethod
    def validate_club(club):
        is_valid = True
        if len(club['name']) == 0:
            is_valid = False
            flash("Please enter a movie title", "name")
        if len(club['name']) > 50:
            is_valid = False
            flash("Club name too long, please write less than 50 characters", "name")
        if len(club['description']) < 3:
            is_valid = False
            flash("Club description too short, please write at least 3 characters", "des")
        if len(club['description']) > 100:
            is_valid = False
            flash("Club description too long, please write no more than 100 characters", "des")
        return is_valid
    
    @staticmethod
    def validate_club_genre(genre):
        is_valid_genre = True
        if len(genre) == 0 or len(genre) > 1:
            is_valid_genre = False
            flash("Please choose one category", "gen")
        return is_valid_genre