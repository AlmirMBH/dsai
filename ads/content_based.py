from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from config import CONTENT_BASED_MIN_SIMILARITY, CONTENT_BASED_MIN_RATERS, CONTENT_BASED_MIN_RATING

class ContentBasedRecommender:
    """
    Recommend movies based on content similarity using semantic vectorization.
    Score movies by cosine similarity, see functions below.
    """
    def __init__(self, graph, movies_df):
        """
        Initialize the recommender and vectorize all movie titles using semantic model.
        Map movie ID to its index in the dataframe to find a movie's vector via its ID.
        """
        self.graph = graph
        self.movies_df = movies_df
        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
        movie_titles = list(self.movies_df['title'])
        self.movie_vectors = self.semantic_model.encode(movie_titles)
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
        movie_scores = {}
        sorted_movies = []
        user_movie_indices = []

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
            # Slice [idx:idx+1] gets one row but keeps it as 2D array shape required by cosine_similarity
            # +1 because slicing is [start:end) where end is exclusive, so idx+1 gives exactly one row
            movie_vector = self.movie_vectors[movie_idx:movie_idx+1]        
            similarity_scores = cosine_similarity(movie_vector, user_vectors)
            max_similarity = similarity_scores.max()            
            users_who_watched = self.graph.get_movie_users(movie_id)

            if max_similarity > CONTENT_BASED_MIN_SIMILARITY and len(users_who_watched) >= CONTENT_BASED_MIN_RATERS:
                ratings = []
                for user in users_who_watched:
                    rating = self.graph.get_rating(user, movie_id)
                    ratings.append(rating)
                avg_rating = sum(ratings) / len(ratings)
                if avg_rating >= CONTENT_BASED_MIN_RATING:
                    final_score = max_similarity * avg_rating
                    movie_scores[movie_id] = (max_similarity, avg_rating, final_score)
        
        movie_list = list(movie_scores.items())
        movie_list.sort(key=lambda item: item[1][2], reverse=True)
        
        for i in range(min(top_k, len(movie_list))):
            movie_id = movie_list[i][0]
            similarity = movie_list[i][1][0]
            rating = movie_list[i][1][1]
            score_tuple = (similarity, rating)
            sorted_movies.append((movie_id, score_tuple))
        
        return sorted_movies