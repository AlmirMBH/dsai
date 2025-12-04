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

# This is the main file where the app starts. We load the data,
# initialize the recommenders, show recommendations and the graph
# and create the UI. See README.md for the project setup and
# more details about how the project works.
ratings_df = pd.read_csv(RATINGS_FILE)
graph = BipartiteGraph(ratings_df)
movies_df = pd.read_csv(MOVIES_FILE)

collaborative_recommender = CollaborativeRecommender(graph)
cold_start_recommender = ColdStartRecommender(graph)
content_based_recommender = ContentBasedRecommender(graph, movies_df)
same_genre_recommender = SameGenreRecommender(graph, movies_df)

st.title("Movie Recommendation System")
# Dropdown limited to MAX_USERS (too long otherwise).
user_ids = sorted(graph.get_user_ids())[:MAX_USERS]

if DEFAULT_DROP_DOWN_USER_ID in user_ids:
    default_index = user_ids.index(DEFAULT_DROP_DOWN_USER_ID)
else:
    default_index = 0

selected_user = st.selectbox("Select User ID", user_ids, index=default_index)
recommender_type = st.selectbox("Recommender Algorithm", ["Collaborative", "Content-Based", "Same-Genre", "Cold-Start"])

@st.cache_data
def get_recommendations(user_id, recommender_type, top_k):
    if recommender_type == "Collaborative":
        return collaborative_recommender.recommend(user_id, top_k)
    elif recommender_type == "Content-Based":
        return content_based_recommender.recommend(user_id, top_k)
    elif recommender_type == "Same-Genre":
        return same_genre_recommender.recommend(user_id, top_k)
    else:
        return cold_start_recommender.recommend(user_id, top_k)

if selected_user:
    if recommender_type == "Collaborative":
        recommendations, recommended_movie_ids, similar_users = get_recommendations(selected_user, recommender_type, RECOMMENDATION_TOP_K)
    else:
        recommendations = get_recommendations(selected_user, recommender_type, RECOMMENDATION_TOP_K)
    
    if recommender_type == "Cold-Start":
        score_text = "number of users who watched this movie"
    elif recommender_type == "Collaborative":
        score_text = "similar users and their ratings of the movie"
    elif recommender_type == "Content-Based":
        score_text = "similarity to your past watches"
    elif recommender_type == "Same-Genre":  
        score_text = "average rating"

    st.subheader(f"Top {RECOMMENDATION_TOP_K} Recommendations")
    st.write(f"***(Score based on: {score_text})***")

    for movie_id, score in recommendations:
        movie_rows = movies_df[movies_df['movieId'] == movie_id]
        movie_info = movie_rows.iloc[0]
        movie_title = movie_info['title']

        if recommender_type == "Cold-Start":
            result = f"**{movie_title}**  --  {score}"
        elif recommender_type == "Content-Based":
            result = f"**{movie_title}**  --  {score*100:.1f}%"
        elif (recommender_type == "Collaborative"
             or recommender_type == "Same-Genre"):
            result = f"**{movie_title}**  --  {score:.1f}"
        st.write(result)
    
    # Only collaborative filtering has user-movie relationships.
    if recommender_type == "Collaborative":
        st.subheader("Graph Visualization")
        G = nx.Graph()
        
        # Edges added from the selected user to recommended movies.
        selected_user_node = f"U{selected_user}"
        G.add_node(selected_user_node, node_type="selected_user")
        
        for user_id in similar_users:
            user_node = f"U{user_id}"
            G.add_node(user_node, node_type="similar_user")
        
        for movie_id in recommended_movie_ids:
            movie_node = f"M{movie_id}"
            G.add_node(movie_node, node_type="recommended_movie")
        
        for movie_id in recommended_movie_ids:
            movie_node = f"M{movie_id}"
            G.add_edge(selected_user_node, movie_node)
        
        # Edges between similar users and recommended movies.
        for user_id in similar_users:
            user_node = f"U{user_id}"
            movies_watched_by_user = graph.get_user_movies(user_id)

            for movie_id in movies_watched_by_user:
                movie_node = f"M{movie_id}"
                if G.has_node(movie_node):
                    G.add_edge(user_node, movie_node)
        
        # Here we use spring_layout to map each node to (x, y) coordinates
        # for arranging nodes in the graph: k=1 sets the target spacing
        # between nodes, and iterations=50 runs 50 adjustment steps, moving
        # nodes until forces balance and the layout settles into stable positions.
        # Then, we filter nodes by type to color them differently.
        pos = nx.spring_layout(G, k=1, iterations=50)
        selected_node = [selected_user_node]
        similar_user_nodes = []
        recommended_movie_nodes = []

        for node in G.nodes():
            node_data = G.nodes[node]
            if node_data['node_type'] == 'similar_user':
                similar_user_nodes.append(node)
            elif node_data['node_type'] == 'recommended_movie':
                recommended_movie_nodes.append(node)
        
        plt.figure()
        nx.draw_networkx_nodes(G, pos, nodelist=selected_node, node_color='red', node_size=200)
        nx.draw_networkx_nodes(G, pos, nodelist=similar_user_nodes, node_color='lightblue', node_size=100)
        nx.draw_networkx_nodes(G, pos, nodelist=recommended_movie_nodes, node_color='green', node_size=150)
        
        # Draw connections between nodes, and add a legend.
        # Hide axes as they are not needed.
        nx.draw_networkx_edges(G, pos)
        plt.legend(['Selected User', 'Similar Users', 'Recommended Movies'], loc='upper right', fontsize=6)
        plt.axis('off')
        st.pyplot(plt)