class ColdStartRecommender:
    """
    Here we recommend most popular movies to users who have no rating history.
    This is how we solve so-called cold-start problem which cannot be solved by
    collaborative filtering. The principle is simple:
    We fetch the movies that the user watched (if any). Then we fetch all movies
    and find those that the user has not watched (to recommend).
    Finally, we sort movies by popularity (number of users who watched them)
    and return the top_k. The score is the number of users who watched the movie.
    """
    def __init__(self, graph):
        self.graph = graph
    
    def recommend(self, user_id, top_k=10):
        movie_counts = {}
        unseen_movies = {}

        for movie_id in self.graph.get_movie_ids():
            users_who_watched = self.graph.get_movie_users(movie_id)
            movie_counts[movie_id] = len(users_who_watched)
        
        user_movies = self.graph.get_user_movies(user_id)
        
        for movie_id, count in movie_counts.items():
            if movie_id not in user_movies:
                unseen_movies[movie_id] = count
        
        return sorted(unseen_movies.items(), key=lambda item: item[1], reverse=True)[:top_k]

