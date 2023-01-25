from movieclubs.conf.mysqlconnection import connectToMySQL
from movieclubs.models import users_model

class Post:
    
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.users_id = data['users_id']
        self.clubs_id = data['clubs_id']
        self.created_at = data['created_at']
        
    @classmethod
    def get_posts(cls,data):
        query = """SELECT * FROM posts JOIN users ON posts.users_id = users.id
                    WHERE posts.clubs_id = %(id)s;"""
        results = connectToMySQL('movieclub').query_db(query, data)
        posts = []
        for post in results:
            one_post = cls(post)
            user = {"id" : post["users.id"],
                    'first_name': post['first_name'],
                    'last_name' : post['last_name'],
                    'username' : post['username'],
                    'email': post['email'],
                    'fav_genre1' : post['fav_genre1'],
                    'fav_genre2' : post['fav_genre2'],
                    'fav_genre3' : post['fav_genre3'],
                    'bio' : post['bio'],
                    'password' : None}
            one_post.poster = users_model.User(user)
            posts.append( one_post )
        return posts
    
    @classmethod
    def deletepostsfromclub(cls,data):
        query = """DELETE FROM posts 
                    WHERE posts.clubs_id = %(id)s;"""
        return connectToMySQL('movieclub').query_db(query, data)
    
    @classmethod
    def save(cls,data):
        query = """INSERT INTO posts (content, users_id, clubs_id)
                   VALUES (%(content)s, %(users_id)s, %(clubs_id)s);"""
        return connectToMySQL('movieclub').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM posts WHERE posts.id = %(id)s;"
        return connectToMySQL('MovieClub').query_db(query, data)