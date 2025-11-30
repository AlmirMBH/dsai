from config import MAX_SIMILAR_USERS

class CollaborativeRecommender:
    def __init__(self, graph):
        self.graph = graph
    
    def score_movie(self, user_id, movie_id):
        # Fetch user (to whom we are recommending) movies and check if the user watched it,
        # if so, return score 0 (do not recommend it again)
        user_movies = self.graph.get_user_movies(user_id)
        if movie_id in user_movies:
            return 0
        
        total_score = 0.0
        
        # Fetch users who watched this movie (potentially similar users).
        users_who_watched_movie = self.graph.get_movie_users(movie_id)
        
        # Fetch watched movies that the other user watched and find if there are
        # movies that both users watched. If not, skip this user because
        # we cannot calculate the similarity between the two users.
        for other_user_id in users_who_watched_movie:
            other_user_movies = self.graph.get_user_movies(other_user_id)
            common_movies = user_movies & other_user_movies

            if len(common_movies) == 0:
                continue
            
            # Calculate Jaccard similarity (two users' movie preferences overlap ratio):
            # similarity = common_movies / (user_movies + other_user_movies - common_movies)
            num_common_movies = len(common_movies)
            num_user_movies = len(user_movies)
            num_other_user_movies = len(other_user_movies)
            total_unique_movies = num_user_movies + num_other_user_movies - num_common_movies
            similarity = num_common_movies / total_unique_movies
            
            # Get the rating that the other user gave to the movie.
            # Add the weighted contribution: similarity * rating            
            other_user_rating = self.graph.get_rating(other_user_id, movie_id)
            weighted_contribution = similarity * other_user_rating
            total_score += weighted_contribution
        
        return total_score
    
    
    def pick_users_for_movies(self, similar_users, recommended_movie_ids, max_users_per_movie):
        all_picked_users = []
        
        # Here we just pick users to show with movies in the graph (not for recommendations).
        # Track which users have already been selected to avoid duplicates (if possible)
        # across different movies.
        used_users = set()
        
        # For each recommended movie, pick users who watched it.
        # Retain users from the similar_users set only (collaborative filtering).
        for movie_id in recommended_movie_ids:
            users_who_watched_movie = self.graph.get_movie_users(movie_id)
            relevant_users = []

            for user_id in similar_users:
                if user_id in users_who_watched_movie:
                    relevant_users.append(user_id)
            
            # First, pick users we haven't shown for other movies yet
            # (this makes the graph show different users for each movie).
            picked_for_this_movie = []

            # From relevant users keep those that were not used with other
            # movies yet, and stop if the maximum number
            # of users per movie reached.
            for user_id in relevant_users:
                if len(picked_for_this_movie) >= max_users_per_movie:
                    break
                
                if user_id not in used_users:
                    picked_for_this_movie.append(user_id)
                    used_users.add(user_id)
            
            # If not enough users for this movie, add already-used users.
            if len(picked_for_this_movie) < max_users_per_movie:
                for user_id in relevant_users:
                    if len(picked_for_this_movie) >= max_users_per_movie:
                        break
                    
                    if user_id not in picked_for_this_movie:
                        picked_for_this_movie.append(user_id)
            
            all_picked_users.extend(picked_for_this_movie)
        
        return all_picked_users
    

    def recommend(self, user_id, top_k=10):
        similar_users = set()
        movie_scores = []
        recommended_movie_ids = []

        # Get all movies that the user watched and find similar users (overlapping movies).        
        user_movies = self.graph.get_user_movies(user_id)

        for movie_id in user_movies:
            users_who_watched_this_movie = self.graph.get_movie_users(movie_id)            
            similar_users.update(users_who_watched_this_movie)
        
        similar_users.discard(user_id)
        
        # Get all movies and find those that the user has not watched (potential recommendations).
        all_movies = set(self.graph.movie_users.keys())
        unseen_movies = all_movies - user_movies
        
        # Score each unseen movie (see score_movie method above).
        for movie_id in unseen_movies:
            score = self.score_movie(user_id, movie_id)
            movie_scores.append((movie_id, score))
        
        # Sort movies by score in descending order (highest scores first).
        movie_scores.sort(key=lambda item: item[1], reverse=True)
        
        # Select the top_k (specified in the config.py) movies.
        recommendations = movie_scores[:top_k]
        
        for movie_id, score in recommendations:
            recommended_movie_ids.append(movie_id)
        
        # These users are displayed in the graph, so that it is visible
        # why specific movies were recommended.
        similar_users_for_viz = self.pick_users_for_movies(similar_users, recommended_movie_ids, MAX_SIMILAR_USERS)
        
        return recommendations, recommended_movie_ids, similar_users_for_viz

