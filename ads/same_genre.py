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
        sorted_movies = []

        user_movies = self.graph.get_user_movies(user_id)
                
        for movie_id in user_movies:
            movie_genres = self.movie_genres.get(movie_id, set())
            user_genres.update(movie_genres)
        
        all_movies = set(self.graph.get_movie_ids())
        unseen_movies = all_movies - user_movies
        
        for movie_id in unseen_movies:
            movie_genres = self.movie_genres.get(movie_id, set())
            shared_genres = user_genres & movie_genres
            
            if len(shared_genres) >= 2:
                users_who_watched = self.graph.get_movie_users(movie_id)
                
                if len(users_who_watched) >= 30:
                    ratings = []
                    for user_id_who_watched in users_who_watched:
                        rating = self.graph.get_rating(user_id_who_watched, movie_id)
                        ratings.append(rating)
                    
                    average_rating = sum(ratings) / len(ratings) if ratings else 0
                    if average_rating >= 3.8:
                        genre_count = len(shared_genres)
                        # Popularity boost: scales 0-1.0 based on watchers (100+ watchers = max boost of 1.0)
                        # Prevents blockbusters from dominating, e.g. 50 watchers = 0.5, 200 watchers = 1.0
                        popularity_boost = min(len(users_who_watched) / 100, 1.0)
                        final_score = average_rating * genre_count * (1 + popularity_boost)
                        movie_scores[movie_id] = (average_rating, genre_count, popularity_boost, final_score)
        
        movie_list = list(movie_scores.items())
        movie_list.sort(key=lambda item: item[1][3], reverse=True)
        
        for i in range(min(top_k, len(movie_list))):
            movie_id = movie_list[i][0]
            rating = movie_list[i][1][0]
            genre_count = movie_list[i][1][1]
            popularity_boost = movie_list[i][1][2]
            score_tuple = (rating, genre_count, popularity_boost)
            sorted_movies.append((movie_id, score_tuple))
        
        return sorted_movies

