import pandas as pd
from collections import defaultdict

class BipartiteGraph:
    def __init__(self, ratings_file):
        ratings = pd.read_csv(ratings_file)
        
        self.user_movies = defaultdict(set)
        self.movie_users = defaultdict(set)
        self.user_ratings = defaultdict(dict)
        
        for _, row in ratings.iterrows():
            user_id = int(row['userId'])
            movie_id = int(row['movieId'])
            rating = float(row['rating'])
            
            self.user_movies[user_id].add(movie_id)
            self.movie_users[movie_id].add(user_id)
            self.user_ratings[user_id][movie_id] = rating
    
    def get_user_movies(self, user_id):
        return self.user_movies.get(user_id, set())
    
    def get_movie_users(self, movie_id):
        return self.movie_users.get(movie_id, set())
    
    def get_rating(self, user_id, movie_id):
        return self.user_ratings.get(user_id, {}).get(movie_id, 0)

