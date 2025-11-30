import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedRecommender:
    def __init__(self, graph, movies_file):
        self.graph = graph
        self.movies_df = pd.read_csv(movies_file)
        self.vectorizer = TfidfVectorizer()
        self.movie_vectors = self.vectorizer.fit_transform(self.movies_df['title'])
        self.movie_id_to_idx = {int(row['movieId']): idx for idx, row in self.movies_df.iterrows()}
    
    def recommend(self, user_id, top_k=10):
        user_movies = self.graph.get_user_movies(user_id)
        user_indices = [self.movie_id_to_idx[mid] for mid in user_movies if mid in self.movie_id_to_idx]
        user_vectors = self.movie_vectors[user_indices]
        
        scores = {}
        all_movies = set(self.graph.movie_users.keys())
        for mid in all_movies - user_movies:
            if mid in self.movie_id_to_idx:
                movie_vec = self.movie_vectors[self.movie_id_to_idx[mid]]
                similarity = cosine_similarity(movie_vec, user_vectors).max()
                if similarity > 0:
                    scores[mid] = similarity
        
        sorted_movies = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_movies[:top_k]

