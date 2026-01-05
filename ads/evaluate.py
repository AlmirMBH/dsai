import pandas as pd
import numpy as np
import time
from graph import BipartiteGraph
from collaborative import CollaborativeRecommender
from content_based import ContentBasedRecommender
from same_genre import SameGenreRecommender
from cold_start import ColdStartRecommender
from config import RATINGS_FILE, MOVIES_FILE

def evaluate(recommender, test_dataframe, top_k=10, user_limit=10):
    precision_list, recall_list, f1_list, hit_list = [], [], [], []
    test_dictionary = test_dataframe.groupby('userId')['movieId'].apply(set).to_dict()
    train_user_ids = set(recommender.graph.get_user_ids())
    evaluated_users = [user_id for user_id in test_dictionary.keys() if user_id in train_user_ids][:user_limit]
    
    for user_id in evaluated_users:
        actual_movies = test_dictionary[user_id]
        result = recommender.recommend(user_id, top_k=top_k)
        recommended_movies = [movie[0] for movie in (result[0] if isinstance(result, tuple) else result)]
        intersection = set(recommended_movies) & actual_movies
        precision = len(intersection) / top_k
        recall = len(intersection) / len(actual_movies)
        precision_list.append(precision)
        recall_list.append(recall)
        f1_list.append(2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0)
        hit_list.append(1 if intersection else 0)
    return np.mean(precision_list), np.mean(recall_list), np.mean(f1_list), np.mean(hit_list)

if __name__ == "__main__":
    ratings_dataframe = pd.read_csv(RATINGS_FILE).sample(frac=1, random_state=42)
    movies_dataframe = pd.read_csv(MOVIES_FILE)
    split_index = int(len(ratings_dataframe) * 0.8)
    training_dataframe, testing_dataframe = ratings_dataframe.iloc[:split_index], ratings_dataframe.iloc[split_index:]
    bipartite_graph = BipartiteGraph(training_dataframe)
    recommender_instances = {
        "Collaborative": CollaborativeRecommender(bipartite_graph),
        "Content-Based": ContentBasedRecommender(bipartite_graph, movies_dataframe),
        "Same-Genre": SameGenreRecommender(bipartite_graph, movies_dataframe),
        "Cold-Start": ColdStartRecommender(bipartite_graph)
    }

    print(f"{'Algorithm':<15} | {'Precision@K':<11} | {'Recall@K':<9} | {'F1@K':<8} | {'HitRate':<8}")
    print("-" * 65)
    evaluation_start_time = time.time()
    for algorithm_name, recommender_instance in recommender_instances.items():
        evaluation_metrics = evaluate(recommender_instance, testing_dataframe)
        print(f"{algorithm_name:<15} | {evaluation_metrics[0]:<11.4f} | {evaluation_metrics[1]:<9.4f} | {evaluation_metrics[2]:<8.4f} | {evaluation_metrics[3]:<8.4f}")

    print(f"\nTotal time: {time.time() - evaluation_start_time:.2f} seconds")
