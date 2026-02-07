import numpy as np
import time
from graph import BipartiteGraph
from collaborative import CollaborativeRecommender
from content_based import ContentBasedRecommender
from same_genre import SameGenreRecommender
from config import EVALUATION_TOP_K, EVALUATION_USER_LIMIT, TRAIN_TEST_SPLIT_RATIO

def evaluate(recommender, test_dataframe, top_k=10, user_limit=10):
    """
    Metrics:
    TP (True Positive) = recommended AND in test set (correct recommendation)
    FP (False Positive) = recommended BUT NOT in test set (wrong recommendation)
    FN (False Negative) = NOT recommended BUT in test set (missed movie)
    TN (True Negative) = NOT recommended AND NOT in test set (not used in these metrics)
    Precision = TP / (TP + FP) = correct / total_recommended
    Recall = TP / (TP + FN) = correct / total_actual
    F1 = 2 * (Precision * Recall) / (Precision + Recall)
    Hit Rate = 1 if at least one TP, else 0
    """
    f1_list = []
    hit_list = []
    recall_list = []
    precision_list = []
    test_dictionary = {}
    evaluated_users = []
    recommended_movies = []
    
    grouped_by_user = test_dataframe.groupby('userId')['movieId']

    for user_id, movie_ids in grouped_by_user:
        test_dictionary[user_id] = set(movie_ids)
    
    train_user_ids = set(recommender.graph.get_user_ids())
    
    for user_id in test_dictionary.keys():
        if user_id in train_user_ids:
            evaluated_users.append(user_id)
            if len(evaluated_users) >= user_limit:
                break
    
    for user_id in evaluated_users:
        actual_movies = test_dictionary[user_id]
        result = recommender.recommend(user_id, top_k=top_k)
        
        if isinstance(result, tuple):
            recommendations = result[0]
        else:
            recommendations = result
        
        
        for movie in recommendations:
            movie_id = movie[0]
            recommended_movies.append(movie_id)
        
        intersection = set(recommended_movies) & actual_movies
        precision = len(intersection) / top_k
        recall = len(intersection) / len(actual_movies)
        precision_list.append(precision)
        recall_list.append(recall)
        
        if precision + recall > 0:
            f1_score = 2 * precision * recall / (precision + recall)
        else:
            f1_score = 0
        f1_list.append(f1_score)
        
        if intersection:
            hit_list.append(1)
        else:
            hit_list.append(0)

    return np.mean(precision_list), np.mean(recall_list), np.mean(f1_list), np.mean(hit_list)


def run_initial_evaluations(ratings_dataframe, movies_dataframe):
    shuffled_ratings = ratings_dataframe.sample(frac=1, random_state=42)
    split_index = int(len(shuffled_ratings) * TRAIN_TEST_SPLIT_RATIO)
    training_dataframe = shuffled_ratings.iloc[:split_index]
    testing_dataframe = shuffled_ratings.iloc[split_index:]
    evaluation_graph = BipartiteGraph(training_dataframe)
    
    evaluation_recommenders = {}
    evaluation_recommenders["Collaborative"] = CollaborativeRecommender(evaluation_graph)
    evaluation_recommenders["Content-Based"] = ContentBasedRecommender(evaluation_graph, movies_dataframe)
    evaluation_recommenders["Same-Genre"] = SameGenreRecommender(evaluation_graph, movies_dataframe)
    
    start_time = time.time()
    results = {}
    
    for name, recommender in evaluation_recommenders.items():
        results[name] = evaluate(recommender, testing_dataframe, EVALUATION_TOP_K, EVALUATION_USER_LIMIT)
    
    duration = time.time() - start_time
    
    return results, testing_dataframe, evaluation_recommenders, duration