import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from graph import BipartiteGraph
from collaborative import CollaborativeRecommender
from cold_start import ColdStartRecommender
from content_based import ContentBasedRecommender
from same_genre import SameGenreRecommender
from config import RATINGS_FILE, MOVIES_FILE, RECOMMENDATION_TOP_K, MAX_USERS

graph = BipartiteGraph(RATINGS_FILE)
collaborative_recommender = CollaborativeRecommender(graph)
cold_start_recommender = ColdStartRecommender(graph)
content_based_recommender = ContentBasedRecommender(graph, MOVIES_FILE)
same_genre_recommender = SameGenreRecommender(graph, MOVIES_FILE)
movies_df = pd.read_csv(MOVIES_FILE)

st.title("Movie Recommendation System")

user_ids = sorted(graph.user_movies.keys())[:MAX_USERS]
selected_user = st.selectbox("Select User ID", user_ids, index=user_ids.index(5) if 5 in user_ids else 0)
recommender_type = st.selectbox("Recommender Algorithm", ["Collaborative", "Content-Based", "Same-Genre", "Cold-Start"])

if selected_user:
    if recommender_type == "Collaborative":
        recommendations, recommended_movie_ids, similar_users = collaborative_recommender.recommend(selected_user, RECOMMENDATION_TOP_K)
    elif recommender_type == "Content-Based":
        recommendations = content_based_recommender.recommend(selected_user, RECOMMENDATION_TOP_K)
    elif recommender_type == "Same-Genre":
        recommendations = same_genre_recommender.recommend(selected_user, RECOMMENDATION_TOP_K)
    else:
        recommendations = cold_start_recommender.recommend(selected_user, RECOMMENDATION_TOP_K)
        print(recommendations)
    
    st.subheader("Top Recommendations")
    for movie_id, score in recommendations:
        movie_info = movies_df[movies_df['movieId'] == movie_id].iloc[0]
        st.write(f"**{movie_info['title']}** - Score: {score:.1f}")
    
    if recommender_type == "Collaborative":
        st.subheader("Graph Visualization")
        
        G = nx.Graph()
        G.add_node(f"U{selected_user}", node_type="selected_user")
        for uid in similar_users:
            G.add_node(f"U{uid}", node_type="similar_user")
        for mid in recommended_movie_ids:
            G.add_node(f"M{mid}", node_type="recommended_movie")
        
        for mid in recommended_movie_ids:
            G.add_edge(f"U{selected_user}", f"M{mid}")
        for uid in similar_users:
            for mid in graph.get_user_movies(uid):
                if G.has_node(f"M{mid}"):
                    G.add_edge(f"U{uid}", f"M{mid}")
        
        pos = nx.spring_layout(G, k=1, iterations=50)
        selected_node = [f"U{selected_user}"]
        similar_user_nodes = [n for n in G.nodes() if G.nodes[n]['node_type'] == 'similar_user']
        recommended_movie_nodes = [n for n in G.nodes() if G.nodes[n]['node_type'] == 'recommended_movie']
        
        plt.figure()
        nx.draw_networkx_nodes(G, pos, nodelist=selected_node, node_color='red', node_size=300)
        nx.draw_networkx_nodes(G, pos, nodelist=similar_user_nodes, node_color='lightblue', node_size=100)
        nx.draw_networkx_nodes(G, pos, nodelist=recommended_movie_nodes, node_color='green', node_size=150)
        nx.draw_networkx_edges(G, pos)
        plt.legend(['Selected User', 'Similar Users', 'Recommended Movies'], loc='upper left', fontsize=8)
        plt.axis('off')
        st.pyplot(plt)

