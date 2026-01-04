import pandas as pd
import numpy as np
import time
from graph import BipartiteGraph
from collaborative import CollaborativeRecommender
from content_based import ContentBasedRecommender
from same_genre import SameGenreRecommender
from cold_start import ColdStartRecommender
from config import RATINGS_FILE, MOVIES_FILE

def evaluate(recommender, test_df, top_k=10, user_limit=10):
    precision_list, recall_list, f1_list, hit_list = [], [], [], []
    test_dict = test_df.groupby('userId')['movieId'].apply(set).to_dict()
    train_user_ids = set(recommender.graph.get_user_ids())
    # Evaluate only users that have history in training set for fair comparison
    evaluated_users = [uid for uid in test_dict.keys() if uid in train_user_ids][:user_limit]
    
    for user_id in evaluated_users:
        actual_movies = test_dict[user_id]
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

ratings_dataframe = pd.read_csv(RATINGS_FILE).sample(frac=1, random_state=42)
movies_dataframe = pd.read_csv(MOVIES_FILE)
split_index = int(len(ratings_dataframe) * 0.8)
train_df, test_df = ratings_dataframe.iloc[:split_index], ratings_dataframe.iloc[split_index:]
graph = BipartiteGraph(train_df)
recommenders = {
    "Collaborative": CollaborativeRecommender(graph),
    "Content-Based": ContentBasedRecommender(graph, movies_dataframe),
    "Same-Genre": SameGenreRecommender(graph, movies_dataframe),
    "Cold-Start": ColdStartRecommender(graph)
}

print(f"{'Algorithm':<15} | {'Precision@K':<11} | {'Recall@K':<9} | {'F1@K':<8} | {'HitRate':<8}")
print("-" * 65)
start_time = time.time()
for name, recommender in recommenders.items():
    metrics = evaluate(recommender, test_df)
    print(f"{name:<15} | {metrics[0]:<11.4f} | {metrics[1]:<9.4f} | {metrics[2]:<8.4f} | {metrics[3]:<8.4f}")

print(f"\nTotal time: {time.time() - start_time:.2f} seconds")
