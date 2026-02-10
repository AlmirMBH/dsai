import streamlit as st
import time

@st.cache_resource(show_spinner="Please wait until the datasets are loaded and evaluations performed")
def initialize_recommendation_system():
    import pandas
    import matplotlib.pyplot as matplotlib_pyplot
    import networkx
    from graph import BipartiteGraph
    from collaborative import CollaborativeRecommender
    from cold_start import ColdStartRecommender
    from content_based import ContentBasedRecommender
    from same_genre import SameGenreRecommender
    from evaluate import evaluate, run_initial_evaluations
    from config import RATINGS_FILE, MOVIES_FILE, RECOMMENDATION_TOP_K, MAX_USERS, DEFAULT_DROP_DOWN_USER_ID

    ratings_dataframe = pandas.read_csv(RATINGS_FILE)
    movies_dataframe = pandas.read_csv(MOVIES_FILE)
    bipartite_graph = BipartiteGraph(ratings_dataframe)
    
    results, testing_dataframe, evaluation_recommenders, duration = run_initial_evaluations(ratings_dataframe, movies_dataframe)

    return (ratings_dataframe, movies_dataframe, bipartite_graph, results, duration,
            pandas, matplotlib_pyplot, networkx, BipartiteGraph, CollaborativeRecommender, 
            ColdStartRecommender, ContentBasedRecommender, SameGenreRecommender, evaluate,
            RECOMMENDATION_TOP_K, MAX_USERS, DEFAULT_DROP_DOWN_USER_ID, 
            testing_dataframe, evaluation_recommenders)

(ratings_dataframe, movies_dataframe, graph, initial_results, initial_duration,
 pandas, matplotlib_pyplot, networkx, BipartiteGraph, CollaborativeRecommender, 
 ColdStartRecommender, ContentBasedRecommender, SameGenreRecommender, evaluate,
 RECOMMENDATION_TOP_K, MAX_USERS, DEFAULT_DROP_DOWN_USER_ID,
 testing_dataframe, evaluation_recommenders) = initialize_recommendation_system()

if "evaluation_results" not in st.session_state:
    st.session_state.evaluation_results = initial_results
    st.session_state.evaluation_duration = initial_duration

collaborative_recommender = CollaborativeRecommender(graph)
cold_start_recommender = ColdStartRecommender(graph)
content_based_recommender = ContentBasedRecommender(graph, movies_dataframe)
same_genre_recommender = SameGenreRecommender(graph, movies_dataframe)

recommendation_tab, evaluation_tab = st.tabs(["Recommendations", "Evaluations"])

with evaluation_tab:
    user_limit = st.selectbox("Users to test", range(1, 101), index=49)
    top_k_value = st.selectbox("K value", range(1, 31), index=9)
    if st.button("Evaluate"):
        with st.status("Wait while evaluations are processed, this will take around 2 minutes"):
            start_time = time.time()
            results = {}
            for name, recommender in evaluation_recommenders.items():
                results[name] = evaluate(recommender, testing_dataframe, top_k_value, user_limit)
            st.session_state.evaluation_results = results
            st.session_state.evaluation_duration = time.time() - start_time
    
    if "evaluation_results" in st.session_state:
        st.table(pandas.DataFrame(st.session_state.evaluation_results, index=["Precision", "Recall", "F1", "HitRate"]).T)
        st.write(f"Total time: {st.session_state.evaluation_duration:.2f} seconds")

with recommendation_tab:
    st.title("Movie Recommendation System")
    user_ids = sorted(graph.get_user_ids())[:MAX_USERS]
    default_index = user_ids.index(DEFAULT_DROP_DOWN_USER_ID) if DEFAULT_DROP_DOWN_USER_ID in user_ids else 0

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
        
        score_texts = {
            "Cold-Start": "number of users who watched this movie", 
            "Collaborative": "user similarity multiplied by the movie rating", 
            "Content-Based": "title similarity and movie rating", 
            "Same-Genre": "rating, genre overlap, and popularity"
        }
        score_text = score_texts.get(recommender_type, "")

        st.subheader(f"Top {RECOMMENDATION_TOP_K} Recommendations")
        st.write(f"***(Score based on: {score_text})***")

        for movie_id, score in recommendations:
            movie_info = movies_dataframe[movies_dataframe['movieId'] == movie_id].iloc[0]
            movie_title = movie_info['title']
            if recommender_type == "Cold-Start":
                result = f"**{movie_title}**  --  {score}"
            elif recommender_type == "Content-Based":
                similarity = score[0]
                rating = score[1]
                result = f"**{movie_title}**  --  Similarity: {similarity*100:.1f}% | Rating: {rating:.1f}"
            elif recommender_type == "Same-Genre":
                rating = score[0]
                genre_count = score[1]
                popularity_boost = score[2]
                result = f"**{movie_title}**  --  Rating: {rating:.1f} | Shared Genres: {genre_count} | Popularity: {popularity_boost*100:.0f}%"
            else:
                display_score = min(score / 100, 0.9)
                result = f"**{movie_title}**  --  {display_score:.2f}"
            st.write(result)
        
        if recommender_type == "Collaborative":
            st.subheader("Graph Visualization")
            graph_visualization = networkx.Graph()
            selected_user_node = f"U{selected_user}"
            graph_visualization.add_node(selected_user_node, node_type="selected_user")
            for user_id in similar_users:
                graph_visualization.add_node(f"U{user_id}", node_type="similar_user")
            for movie_id in recommended_movie_ids:
                graph_visualization.add_node(f"M{movie_id}", node_type="recommended_movie")
                graph_visualization.add_edge(selected_user_node, f"M{movie_id}")
            for user_id in similar_users:
                user_node_id = f"U{user_id}"
                for movie_id in graph.get_user_movies(user_id):
                    if graph_visualization.has_node(f"M{movie_id}"):
                        graph_visualization.add_edge(user_node_id, f"M{movie_id}")
            
            node_positions = networkx.spring_layout(graph_visualization, k=1, iterations=50)
            networkx.draw_networkx_nodes(graph_visualization, node_positions, nodelist=[selected_user_node], node_color='red', node_size=200)
            networkx.draw_networkx_nodes(graph_visualization, node_positions, nodelist=[node_id for node_id, node_data in graph_visualization.nodes(data=True) if node_data.get('node_type') == 'similar_user'], node_color='lightblue', node_size=100)
            networkx.draw_networkx_nodes(graph_visualization, node_positions, nodelist=[node_id for node_id, node_data in graph_visualization.nodes(data=True) if node_data.get('node_type') == 'recommended_movie'], node_color='green', node_size=150)
            networkx.draw_networkx_edges(graph_visualization, node_positions)
            matplotlib_pyplot.legend(['Selected User', 'Similar Users', 'Recommended Movies'], loc='upper right', fontsize=6)
            matplotlib_pyplot.axis('off')
            st.pyplot(matplotlib_pyplot)
