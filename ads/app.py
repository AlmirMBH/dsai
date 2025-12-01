import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from graph import BipartiteGraph
from collaborative import CollaborativeRecommender
from cold_start import ColdStartRecommender
from content_based import ContentBasedRecommender
from same_genre import SameGenreRecommender
from config import RATINGS_FILE, MOVIES_FILE, RECOMMENDATION_TOP_K, MAX_USERS, DEFAULT_DROP_DOWN_USER_ID

# Create the bipartite graph from ratings data user-movie relationships (who watched what).
graph = BipartiteGraph(RATINGS_FILE)

collaborative_recommender = CollaborativeRecommender(graph)
cold_start_recommender = ColdStartRecommender(graph)
content_based_recommender = ContentBasedRecommender(graph, MOVIES_FILE)
same_genre_recommender = SameGenreRecommender(graph, MOVIES_FILE)

# Load movie data from CSV file (see archive/movies.csv).
movies_df = pd.read_csv(MOVIES_FILE)

# Main title of the application.
st.title("Movie Recommendation System")

# Get all user IDs from the graph, sort them and limit to MAX_USERS
# to keep the dropdown manageable (see config.py).
all_user_ids = list(graph.get_user_movies_dict().keys())
sorted_user_ids = sorted(all_user_ids)
user_ids = sorted_user_ids[:MAX_USERS]


if DEFAULT_DROP_DOWN_USER_ID in user_ids:
    default_index = user_ids.index(DEFAULT_DROP_DOWN_USER_ID)
else:
    default_index = 0

selected_user = st.selectbox("Select User ID", user_ids, index=default_index)

# Dropdown for algorithm selection.
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
    
    
    st.subheader("Top Recommendations")
    
    # Recommended movies with their titles and scores (from the loaded dataframe).
    for movie_id, score in recommendations:
        movie_rows = movies_df[movies_df['movieId'] == movie_id]
        movie_info = movie_rows.iloc[0]
        movie_title = movie_info['title']
        st.write(f"**{movie_title}** - Score: {score:.1f}")
    
    # Graph visualization for collaborative filtering (other algorithms do not provide similar_users data).
    if recommender_type == "Collaborative":
        st.subheader("Graph Visualization")
        G = nx.Graph()
        
        # Add the selected user as a node ("U" for user).
        selected_user_node = f"U{selected_user}"
        G.add_node(selected_user_node, node_type="selected_user")
        
        # Add similar users as nodes (users with similar movie preferences).
        for user_id in similar_users:
            user_node = f"U{user_id}"
            G.add_node(user_node, node_type="similar_user")
        
        # Add recommended movies as nodes ("M" for movie).
        for movie_id in recommended_movie_ids:
            movie_node = f"M{movie_id}"
            G.add_node(movie_node, node_type="recommended_movie")
        
        # Add edges from the selected user to all recommended movies.
        for movie_id in recommended_movie_ids:
            movie_node = f"M{movie_id}"
            G.add_edge(selected_user_node, movie_node)
        
        # Get all movies this similar user watched, and add edges to recommended movies only.
        for user_id in similar_users:
            user_node = f"U{user_id}"
            movies_watched_by_user = graph.get_user_movies(user_id)
            
            for movie_id in movies_watched_by_user:
                movie_node = f"M{movie_id}"
            
                if G.has_node(movie_node):
                    G.add_edge(user_node, movie_node)
        
        # Calculate positions for all nodes using spring layout algorithm.
        # This arranges nodes in a visible way.
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Prepare list of nodes for the selected user (for coloring).
        # Filter nodes by type to color them differently (similar_user, recommended_movie).
        # Find all nodes marked as "similar_user".
        selected_node = [selected_user_node]
        similar_user_nodes = []

        for node in G.nodes():
            node_data = G.nodes[node]
            if node_data['node_type'] == 'similar_user':
                similar_user_nodes.append(node)
        
        # Find all nodes marked as "recommended_movie" (color them green).
        recommended_movie_nodes = []
        for node in G.nodes():
            node_data = G.nodes[node]
            if node_data['node_type'] == 'recommended_movie':
                recommended_movie_nodes.append(node)
        
        plt.figure()
        
        # Selected user node in red.
        # Similar user nodes in light blue.
        # Recommended movie nodes in green.
        nx.draw_networkx_nodes(G, pos, nodelist=selected_node, node_color='red', node_size=300)
        nx.draw_networkx_nodes(G, pos, nodelist=similar_user_nodes, node_color='lightblue', node_size=100)
        nx.draw_networkx_nodes(G, pos, nodelist=recommended_movie_nodes, node_color='green', node_size=150)
        
        # Draw all edges (connections between nodes), and add a legend.
        nx.draw_networkx_edges(G, pos)
        plt.legend(['Selected User', 'Similar Users', 'Recommended Movies'], loc='upper left', fontsize=8)
        
        # Hide axes for a clean visualization, and show the plot.
        plt.axis('off')
        st.pyplot(plt)

