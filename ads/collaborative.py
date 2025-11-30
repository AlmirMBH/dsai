from config import MAX_SIMILAR_USERS

class CollaborativeRecommender:
    def __init__(self, graph):
        self.graph = graph
    
    def score_movie(self, user_id, movie_id):
        if movie_id in self.graph.get_user_movies(user_id):
            return 0
        
        score = 0.0
        user_movies = self.graph.get_user_movies(user_id)
        movie_users = self.graph.get_movie_users(movie_id)
        
        for other_user_id in movie_users:
            common_movies = user_movies & self.graph.get_user_movies(other_user_id)
            if len(common_movies) == 0:
                continue
            
            similarity = len(common_movies) / (len(user_movies) + len(self.graph.get_user_movies(other_user_id)) - len(common_movies))
            rating = self.graph.get_rating(other_user_id, movie_id)
            
            score += similarity * rating
        
        return score
    
    def _pick_users_for_movies(self, similar_users, recommended_movie_ids, max_users_per_movie):
        users = []
        used = set()
        for mid in recommended_movie_ids:
            movie_users = [uid for uid in similar_users if uid in self.graph.get_movie_users(mid)]
            picked = []
            for uid in movie_users:
                if len(picked) >= max_users_per_movie:
                    break
                if uid not in used:
                    picked.append(uid)
                    used.add(uid)
            if len(picked) < max_users_per_movie:
                for uid in movie_users:
                    if len(picked) >= max_users_per_movie:
                        break
                    if uid not in picked:
                        picked.append(uid)
            users.extend(picked)
        return users
    
    def recommend(self, user_id, top_k=10):
        user_movies = self.graph.get_user_movies(user_id)
        
        # Find similar users (users who share movies with selected user)
        similar_users = set()
        for mid in user_movies:
            similar_users.update(self.graph.get_movie_users(mid))
        similar_users.discard(user_id)
        
        # Score and select top k movies
        all_movies = set(self.graph.movie_users.keys())
        unseen_movies = all_movies - user_movies
        scores = [(movie_id, self.score_movie(user_id, movie_id)) for movie_id in unseen_movies]
        scores.sort(key=lambda x: x[1], reverse=True)
        recommendations = scores[:top_k]
        
        recommended_movie_ids = [movie_id for movie_id, _ in recommendations]
        similar_users_for_viz = self._pick_users_for_movies(similar_users, recommended_movie_ids, MAX_SIMILAR_USERS)
        
        return recommendations, recommended_movie_ids, similar_users_for_viz

