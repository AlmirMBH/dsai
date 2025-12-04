from config import MAX_SIMILAR_USERS

class CollaborativeRecommender:
    """
    Recommend movies using collaborative filtering based on Jaccard similarity.
    Score movies by weighted ratings from similar users, see functions below.
    """
    def __init__(self, graph):
        self.graph = graph
    
    def score_movie(self, user_id, movie_id):
        """
        This function is based on the Jaccard similarity. We get the user to whom we are
        recommending movies and all the user's movies. For the given unseen movie, we find
        users who watched it, check if they have common movies with the target user
        (to calculate similarity), and score the movie by summing up the multiplication of
        the similarity between the 2 users and the other user's rating.
        The Jaccard similarity (two users' movie overlap ratio) is calculated as:
        total_unique_movies = num_user_movies + num_other_user_movies - num_common_movies
        users_similarity = num_common_movies / total_unique_movies
        For this movie, the score is then calculated as the sum over all similar users:
        movie_score = sum(users_similarity * other_user_rating) for all similar users who
        watched the movie. Finally, we return the total score for this movie.
        """
        user_movies = self.graph.get_user_movies(user_id)
        if movie_id in user_movies:
            return 0
        
        total_score = 0.0
        users_who_watched_movie = self.graph.get_movie_users(movie_id)
        
        for other_user_id in users_who_watched_movie:
            other_user_movies = self.graph.get_user_movies(other_user_id)
            common_movies = user_movies & other_user_movies

            if len(common_movies) == 0:
                continue
            
            num_common_movies = len(common_movies)
            num_user_movies = len(user_movies)
            num_other_user_movies = len(other_user_movies)
            total_unique_movies = num_user_movies + num_other_user_movies - num_common_movies
            similarity = num_common_movies / total_unique_movies
            other_user_rating = self.graph.get_rating(other_user_id, movie_id)
            weighted_contribution = similarity * other_user_rating
            total_score += weighted_contribution
        
        return total_score
    
    
    def pick_users_for_movies(self, similar_users, recommended_movie_ids, max_users_per_movie):
        """
        Here we pick users to display in the graph visualization (not for recommendations).
        For each recommended movie, we select up to max_users_per_movie users from the
        similar_users set who watched the movie. We prioritize users not shown with
        other movies (in the current graph) to increase diversity of users in the graph.
        If there is not enough unique users, we reuse those that are already used in the graph.
        """
        all_picked_users = []
        used_users = set()
        
        for movie_id in recommended_movie_ids:
            users_who_watched_movie = self.graph.get_movie_users(movie_id)
            relevant_users = []
            picked_for_this_movie = []

            for user_id in similar_users:
                if user_id in users_who_watched_movie:
                    relevant_users.append(user_id)

            for user_id in relevant_users:
                if len(picked_for_this_movie) >= max_users_per_movie:
                    break
                
                if user_id not in used_users:
                    picked_for_this_movie.append(user_id)
                    used_users.add(user_id)
            
            if len(picked_for_this_movie) < max_users_per_movie:
                for user_id in relevant_users:
                    if len(picked_for_this_movie) >= max_users_per_movie:
                        break
                    
                    if user_id not in picked_for_this_movie:
                        picked_for_this_movie.append(user_id)
            
            all_picked_users.extend(picked_for_this_movie)
        
        return all_picked_users
    

    def recommend(self, user_id, top_k=10):
        """
        Get all movies that the user watched and find similar users (users who watched
        any of the same movies). Get all movies and find those that the user has not
        watched (potential recommendations). Score each unseen movie (see score_movie
        method above). Sort movies by score in descending order (highest scores first)
        and select the top_k movies. Returns recommendations, recommended movie IDs,
        and similar users for graph visualization.
        """
        similar_users = set()
        movie_scores = []
        recommended_movie_ids = []
        
        user_movies = self.graph.get_user_movies(user_id)

        for movie_id in user_movies:
            users_who_watched_this_movie = self.graph.get_movie_users(movie_id)            
            similar_users.update(users_who_watched_this_movie)
        
        similar_users.discard(user_id)
        all_movies = set(self.graph.get_movie_ids())
        unseen_movies = all_movies - user_movies
        
        for movie_id in unseen_movies:
            score = self.score_movie(user_id, movie_id)
            movie_scores.append((movie_id, score))
        
        movie_scores.sort(key=lambda item: item[1], reverse=True)
        recommendations = movie_scores[:top_k]
        
        for movie_id, score in recommendations:
            recommended_movie_ids.append(movie_id)
        
        similar_users_for_viz = self.pick_users_for_movies(similar_users, recommended_movie_ids, MAX_SIMILAR_USERS)        
        return recommendations, recommended_movie_ids, similar_users_for_viz

