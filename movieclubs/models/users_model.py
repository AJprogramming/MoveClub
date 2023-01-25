from movieclubs.conf.mysqlconnection import connectToMySQL
from flask import flash
from movieclubs.models.clubs_model import Club
from movieclubs.models.posts_model import Post


import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.username = data['username']
        self.password = data['password']
        self.fav_genre1 = data['fav_genre1']
        self.fav_genre2 = data['fav_genre2']
        self.fav_genre3 = data['fav_genre3']
        self.bio = data['bio']
        self.joined_clubs = []
        
        
    @classmethod
    def new_user(cls, data):
        query = """INSERT INTO users 
        (first_name, last_name, username, email, password)
        VALUES(%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s);"""
        return connectToMySQL('movieclub').query_db(query, data)
    
    @classmethod
    def new_user_genre(cls, data):
        query = """UPDATE users
                    SET fav_genre1 = %(fav_genre1)s, fav_genre2 = %(fav_genre2)s, fav_genre3 = %(fav_genre3)s
                    WHERE id = %(id)s;"""
        return connectToMySQL('movieclub').query_db(query, data)
    
    @classmethod
    def new_user_bio(cls, data):
        query = """UPDATE users
                    SET bio = %(bio)s
                    WHERE id = %(id)s;"""
        return connectToMySQL('movieclub').query_db(query, data)
    
    @classmethod
    def get_one(cls, data):
        query = """SELECT * FROM users WHERE id = %(id)s;"""
        results = connectToMySQL('movieclub').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def join_club(cls, data):
        query = """INSERT INTO joined_clubs (users_id, clubs_id)
                    VALUES (%(users_id)s, %(clubs_id)s);"""
        return connectToMySQL('movieclub').query_db(query, data);
    
    
    @classmethod
    def get_joined_clubs(cls, data):
        query = """SELECT * FROM users LEFT JOIN joined_clubs 
                    ON users.id = joined_clubs.users_id LEFT JOIN clubs 
                    ON clubs.id = joined_clubs.clubs_id WHERE users.id = %(id)s;"""
        results = connectToMySQL('movieclub').query_db(query, data)
        user = cls(results[0])
        for row in results:
            if row['clubs.id'] == None:
                break
            data = {
                "id": row['clubs.id'],
                "name": row['name'],
                "genre": row['genre'],
                "description": row['description']
            }
            user.joined_clubs.append(Club(data))
        return user
    
    # @classmethod
    # def leave_club_list(cls)
    
    @classmethod
    def get_email(cls, data):
        query = """SELECT * FROM users WHERE email = %(email)s;"""
        results = connectToMySQL('movieclub').query_db(query,data)
        if len(results) < 1:
            return False
        return User(results[0])
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            is_valid = False
            flash("First name must be at least 3 characters.","reg")
        if len(user['last_name']) < 3:
            is_valid = False
            flash("Last name must be at least 3 characters.","reg")
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash("Invalid Email Address.","reg")
        if len(user['password']) < 10:
            is_valid = False
            flash("Username must be at least 5 characters.", "reg")
        if len(user['password']) < 5:
            is_valid = False
            flash("Password must be at least 8 characters.","reg")
        if not user['password'] == user['check_password']:
            is_valid = False
            flash("Passwords do not match!","reg")
        return is_valid
    
    @staticmethod
    def validate_genres(user):
        is_valid = True
        if len(user) != 3:
            is_valid = False
            flash("Please pick 3 genres", "gen")
        return is_valid
    
    @staticmethod
    def validate_bio(user):
        is_valid = True
        if len(user['bio']) < 3:
            is_valid = False
            flash("Please write at least 3 characters.", "bio")
        if len(user['bio']) > 150:
            is_valid = False
            flash("Please write no more than a hundred 100 characters", "bio")
        return is_valid