import pandas as pd

class SameGenreRecommender:
    def __init__(self, graph, movies_file):
        self.graph = graph
        self.movie_genres = {}
        self.movies_df = pd.read_csv(movies_file) # see archive/movies.csv
                
        # Mapping from movie ID to its genres set for easy
        # comparison (e.g., {"Action", "Adventure", "Sci-Fi"}).        
        # Split genres by "|" to get individual genres, and convert to set
        # for comparisons.
        for i, row in self.movies_df.iterrows():
            movie_id = int(row['movieId'])
            genres_string = str(row['genres'])
            genres_set = set(genres_string.split('|'))
            self.movie_genres[movie_id] = genres_set
    

    def recommend(self, user_id, top_k=10):
        user_genres = set()
        movie_scores = {}
        movie_list = []

        # Get movies that the user watched.
        # Extract genres from movies that the user watched (user's genre preferences).
        user_movies = self.graph.get_user_movies(user_id)
                
        for movie_id in user_movies:
            movie_genres = self.movie_genres.get(movie_id, set())
            user_genres.update(movie_genres)
        
        # Fetch movies the user has not watched (potential recommendations).
        all_movies = set(self.graph.movie_users.keys())
        unseen_movies = all_movies - user_movies
        
        # Check if movies are in user's genres.
        for movie_id in unseen_movies:
            movie_genres = self.movie_genres.get(movie_id, set())
            shared_genres = user_genres & movie_genres
            
            # Get all users who watched this movie and their ratings.
            if len(shared_genres) > 0:
                ratings = []
                users_who_watched = self.graph.get_movie_users(movie_id)
                
                for user_id_who_watched in users_who_watched:
                    rating = self.graph.get_rating(user_id_who_watched, movie_id)
                    ratings.append(rating)
                
                # Calculate average rating (sum of ratings divided by their count)
                # and store it as the score for this movie.
                if len(ratings) > 0:
                    total_rating = sum(ratings)
                    num_ratings = len(ratings)
                    average_rating = total_rating / num_ratings
                else:
                    average_rating = 0
                
                movie_scores[movie_id] = average_rating
        
        # Convert dictionary to list of tuples for sorting because
        # sorted() works on sequences (lists, tuples), not dictionaries.
        for movie_id, score in movie_scores.items():
            movie_list.append((movie_id, score))
        
        # Sort movies by highest ratings first and return the top_k (specified in the config.py).
        sorted_movies = sorted(movie_list, key=lambda item: item[1], reverse=True)
        recommendations = sorted_movies[:top_k]
        
        return recommendations

