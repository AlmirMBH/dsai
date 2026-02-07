from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedRecommender:
    """
    Recommend movies based on content similarity using TF-IDF vectorization.
    Score movies by cosine similarity, see functions below.
    """
    def __init__(self, graph, movies_df):
        """
        Initialize the recommender and vectorize all movie titles using TF-IDF.
        Map movie ID to its index in the dataframe to find a movie's vector via its ID.
        """
        self.graph = graph
        self.movies_df = movies_df
        self.vectorizer = TfidfVectorizer()
        self.movie_vectors = self.vectorizer.fit_transform(self.movies_df['title'])
        self.movie_id_to_idx = {}

        for idx, row in self.movies_df.iterrows():
            movie_id = int(row['movieId'])
            self.movie_id_to_idx[movie_id] = idx
    

    def recommend(self, user_id, top_k=10):
        """
        This recommender algorithm is an extra feature. We fetch the movies that
        the user watched and extract their vectors, see init above. Then, we calculate
        the cosine similarity for each unseen movie by comparing it to the user's watched
        movies. By doing this, we cover all preferences by the user.
        """
        user_movie_indices = []
        movie_scores = {}

        user_movies = self.graph.get_user_movies(user_id)

        for movie_id in user_movies:
            if movie_id in self.movie_id_to_idx:
                idx = self.movie_id_to_idx[movie_id]
                user_movie_indices.append(idx)
        
        user_vectors = self.movie_vectors[user_movie_indices]        
        if user_vectors.shape[0] == 0:
            return []
            
        all_movies = set(self.graph.get_movie_ids())
        unseen_movies = all_movies - user_movies
        
        for movie_id in unseen_movies:
            if movie_id not in self.movie_id_to_idx:
                continue
            
            movie_idx = self.movie_id_to_idx[movie_id]
            movie_vector = self.movie_vectors[movie_idx]
        
            similarity_scores = cosine_similarity(movie_vector, user_vectors)
            max_similarity = similarity_scores.max()
            
            users_who_watched = self.graph.get_movie_users(movie_id)
            if max_similarity > 0.15 and len(users_who_watched) >= 30:
                ratings = [self.graph.get_rating(u, movie_id) for u in users_who_watched]
                avg_rating = sum(ratings) / len(ratings)
                if avg_rating >= 4.0:
                    final_score = max_similarity * avg_rating
                    movie_scores[movie_id] = (max_similarity, avg_rating, final_score)
        
        movie_list = list(movie_scores.items())
        movie_list.sort(key=lambda item: item[1][2], reverse=True)
        
        sorted_movies = []
        for i in range(min(top_k, len(movie_list))):
            movie_id = movie_list[i][0]
            similarity = movie_list[i][1][0]
            rating = movie_list[i][1][1]
            score_tuple = (similarity, rating)
            sorted_movies.append((movie_id, score_tuple))
        
        return sorted_movies