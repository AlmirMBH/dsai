class SameGenreRecommender:
    """
    Recommends movies based on genre similarity to user's watched movies.
    Scores movies by average rating of all users who watched them.
    """
    def __init__(self, graph, movies_df):
        """
        During the initialization of the SameGenreRecommender, we split a movie
        genres by "|" to get individual genres, convert genres to set for
        comparisons, and map movie ID to its genres set.
        """
        self.graph = graph
        self.movie_genres = {}
        self.movies_df = movies_df
        
        for i, row in self.movies_df.iterrows():
            movie_id = int(row['movieId'])
            genres_string = str(row['genres'])
            genres_set = set(genres_string.split('|'))
            self.movie_genres[movie_id] = genres_set
    

    def recommend(self, user_id, top_k=10):
        """
        We get movies that the user watched, extract genres from movies that the
        user watched (user's genre preferences). Then, we fetch movies the user
        has not watched (potential recommendations) and check if they share any
        genres with the user's genre preferences. If they do, we score the movie
        by the average rating of all users who watched the candidate movie and
        return the top_k movies with the highest scores.
        """
        user_genres = set()
        movie_scores = {}

        user_movies = self.graph.get_user_movies(user_id)
                
        for movie_id in user_movies:
            movie_genres = self.movie_genres.get(movie_id, set())
            user_genres.update(movie_genres)
        
        all_movies = set(self.graph.get_movie_ids())
        unseen_movies = all_movies - user_movies
        
        for movie_id in unseen_movies:
            movie_genres = self.movie_genres.get(movie_id, set())
            shared_genres = user_genres & movie_genres
            
            if len(shared_genres) > 0:
                ratings = []
                users_who_watched = self.graph.get_movie_users(movie_id)
                
                for user_id_who_watched in users_who_watched:
                    rating = self.graph.get_rating(user_id_who_watched, movie_id)
                    ratings.append(rating)
            
                movie_scores[movie_id] = sum(ratings) / len(ratings) if ratings else 0
        
        return sorted(movie_scores.items(), key=lambda item: item[1], reverse=True)[:top_k]

