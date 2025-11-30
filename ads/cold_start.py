class ColdStartRecommender:
    def __init__(self, graph):
        self.graph = graph
    
    def recommend(self, user_id, top_k=10):
        # Count how many users watched each movie to find most popular movies.
        movie_counts = {}
        for movie_id in self.graph.movie_users.keys():
            users_who_watched = self.graph.get_movie_users(movie_id)
            movie_counts[movie_id] = len(users_who_watched)
        
        # Fetch all movies that the user watched.
        user_movies = self.graph.get_user_movies(user_id)
        
        # Filter movies that the user did not watched to recommend
        unseen_movies = {}
        for movie_id, count in movie_counts.items():
            if movie_id not in user_movies:
                unseen_movies[movie_id] = count
        
        # Convert dictionary to list of tuples as sorted() works on
        # sequences (lists, sets, etc.), not dictionaries.
        # Sort movies by popularity (number of users who watched them).
        movie_list = []
        for movie_id, count in unseen_movies.items():
            movie_list.append((movie_id, count))
        
        sorted_movies = sorted(movie_list, key=lambda item: item[1], reverse=True)
        
        # Return the top_k (specified in the config.py) most popular movies.
        recommendations = []
        for i in range(min(top_k, len(sorted_movies))):
            movie_id, count = sorted_movies[i]
            recommendations.append((movie_id, count))
        
        return recommendations

