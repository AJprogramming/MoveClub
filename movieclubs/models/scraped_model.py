from movieclubs.conf.mysqlconnection import connectToMySQL


class Scraped:
    
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.releaseyear = data['releaseyear']
        
    @classmethod
    def get_movies(cls):
        query = """SELECT * FROM movietitles;"""
        results = connectToMySQL('movieclub').query_db(query)
        movies = []
        for movie in results:
            movies.append(cls(movie))
        return movies
