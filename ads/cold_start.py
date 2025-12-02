class ColdStartRecommender:
    def __init__(self, graph):
        self.graph = graph
    
    def recommend(self, user_id, top_k=10):
        # Count how many users watched each movie to find most popular movies to recommend.
        movie_counts = {}
        unseen_movies = {}

        for movie_id in self.graph.get_movie_ids():
            users_who_watched = self.graph.get_movie_users(movie_id)
            movie_counts[movie_id] = len(users_who_watched)
        
        # Fetch all movies that the user watched.
        user_movies = self.graph.get_user_movies(user_id)
        
        # Filter movies that the user did not watch (to recommend).
        for movie_id, count in movie_counts.items():
            if movie_id not in user_movies:
                unseen_movies[movie_id] = count
        
        # Sort movies by popularity (number of users who watched them).
        sorted_movies = sorted(unseen_movies.items(), key=lambda item: item[1], reverse=True)
        return sorted_movies[:top_k]

