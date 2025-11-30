import pandas as pd

class SameGenreRecommender:
    def __init__(self, graph, movies_file):
        self.graph = graph
        self.movies_df = pd.read_csv(movies_file)
        self.movie_genres = {}
        for _, row in self.movies_df.iterrows():
            self.movie_genres[int(row['movieId'])] = set(str(row['genres']).split('|'))
    
    def recommend(self, user_id, top_k=10):
        user_movies = self.graph.get_user_movies(user_id)
        user_genres = set()
        for mid in user_movies:
            user_genres.update(self.movie_genres.get(mid, set()))
        
        scores = {}
        all_movies = set(self.graph.movie_users.keys())
        for mid in all_movies - user_movies:
            movie_genres = self.movie_genres.get(mid, set())
            if user_genres & movie_genres:
                ratings = [self.graph.get_rating(uid, mid) for uid in self.graph.get_movie_users(mid)]
                scores[mid] = sum(ratings) / len(ratings) if ratings else 0
        
        sorted_movies = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_movies[:top_k]

