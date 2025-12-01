import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedRecommender:
    def __init__(self, graph, movies_file):
        self.graph = graph
        self.movies_df = pd.read_csv(movies_file) # see archive/movies.csv
        
        # Via TF-IDF vectorizer convert movie titles into numerical vectors.
        # TF-IDF measures how important words are in movie titles.
        self.vectorizer = TfidfVectorizer()
        self.movie_vectors = self.vectorizer.fit_transform(self.movies_df['title'])
        
        # Create a mapping from movie ID to its index in the dataframe.
        # This helps us find a movie's vector when we only know its ID.
        self.movie_id_to_idx = {}

        for idx, row in self.movies_df.iterrows():
            movie_id = int(row['movieId'])
            self.movie_id_to_idx[movie_id] = idx
    

    def recommend(self, user_id, top_k=10):
        user_movie_indices = []
        movie_scores = {}
        movie_list = []

        # Fetch movies that the user watched and dataframe indices for those
        # movies to get their vectors (see above).
        user_movies = self.graph.get_user_movies(user_id)

        for movie_id in user_movies:
            if movie_id in self.movie_id_to_idx:
                idx = self.movie_id_to_idx[movie_id]
                user_movie_indices.append(idx)
        
        # Fetch the vectors for all movies the user watched to
        # get the user's movie preferences.
        # Fetch movies that the user has not watched.
        user_vectors = self.movie_vectors[user_movie_indices]        
        all_movies = set(self.graph.get_movie_users_dict().keys())
        unseen_movies = all_movies - user_movies
        
        # Calculate how similar unseen is to user's watched movies.
        # Skip movies that are not in the dataframe (missing data).
        for movie_id in unseen_movies:
            if movie_id not in self.movie_id_to_idx:
                continue
            
            # Get the vector for the movie (title).
            movie_idx = self.movie_id_to_idx[movie_id]
            movie_vector = self.movie_vectors[movie_idx]
            
            # Calculate cosine similarity between this movie and user's watched
            # movies, and pick the one with the highest similarity.
            similarity_scores = cosine_similarity(movie_vector, user_vectors)
            max_similarity = similarity_scores.max()

            if max_similarity > 0:
                movie_scores[movie_id] = max_similarity
        
        # Dictionary to list of tuples for sorting becasue sorted() works on
        # sequences (lists, tuples), not dictionaries; higher scores first.
        for movie_id, score in movie_scores.items():
            movie_list.append((movie_id, score))
        
        sorted_movies = sorted(movie_list, key=lambda item: item[1], reverse=True)
        recommendations = sorted_movies[:top_k]
        
        return recommendations

