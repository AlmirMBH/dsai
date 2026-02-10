# Movie Recommendation System
Bipartite graph-based movie recommendation system with multiple recommendation strategies (python < 3.14 required).

## Project Background

This project was completed as part of the undergraduate course _Algorithms and Data Structures II_ at the Faculty of Electrical Engineering, University of Sarajevo, under the supervision of Professor Sead Delic. The project implements a movie recommendation system that leverages bipartite graph data structures to model user-movie relationships and applies various graph-based algorithms for generating recommendations. The system is used to demonstrate practical applications of graphs through collaborative filtering, content-based filtering, and genre-based recommendation algorithms, with a Streamlit interface that visualizes the underlying graph structure and recommendation paths (collaborative filtering).

## Technologies

The recommender is built using Python and several libraries:
- **Streamlit**: Web framework for building the interactive user interface and displaying recommendations.
- **NetworkX**: Graph library for creating and manipulating the bipartite graph structure, as well as graph layout algorithms for visualization.
- **pandas**: Data manipulation library for reading and processing CSV files containing movie ratings and metadata.
- **scikit-learn**: Machine learning library used for cosine similarity calculations in the content-based recommender.
- **sentence-transformers**: Semantic embedding library used for vectorizing movie titles with the all-MiniLM-L6-v2 model in the content-based recommender.
- **matplotlib**: Plotting library for rendering the graph visualization with custom node colors and layouts.

## Note: Performance and Caching

The first time the project is run, it might take several seconds to load data and show the graph and recommendations. However, recommendation results are cached using Streamlit's `@st.cache_data`. When you request recommendations for the same user and algorithm combination again, the results are retrieved from cache instantly, improving response time.

## Setup Virtual Environment
```bash
python3.12 -m venv venv
```

## Project Installation
```bash
source venv/bin/activate && pip install -r requirements.txt
```

## Start Project
```bash
source venv/bin/activate && streamlit run app.py --server.port 8510
```

## Project Startup Note
The first time the project is run, loading the datasets and performing initial evaluations may take 2–3 minutes before the project is fully operational.

## Stop Project
Stop: `pkill -f "streamlit run app.py"` or `Ctrl+C`

## Configuration File
The `config.py` file contains system settings. The number of users is pretty low to keep the graph readable (edges and nodes). The way the recommender works is customized in this file.
- **RATINGS_FILE**: Path to the ratings CSV file (default: `archive/ratings.csv`)
- **MOVIES_FILE**: Path to the movies CSV file (default: `archive/movies.csv`)
- **RECOMMENDATION_TOP_K**: Number of top recommendations to return (default: 10)
- **MAX_USERS**: Maximum number of users displayed in the user selection dropdown (default: 50)
- **GRAPH_MAX_USERS_PER_MOVIE**: Number of similar users to show per recommended movie in graph visualization is configurable to keep the visibility of the similar users in the graph. The algorithm prioritizes unique users first, then reuses users if needed.
- **DEFAULT_DROP_DOWN_USER_ID**: Default user ID selected in the dropdown (default: 5)

After making any changes to `config.py`, press the "Rerun" button in the upper right corner of the Streamlit UI to apply and see the changes.


## Dataset
The datasets used in this project are from [MovieLens Latest Small Dataset](https://www.kaggle.com/datasets/grouplens/movielens-latest-small) from Kaggle. There are ratings.csv (user-movie ratings) and movies.csv (movie titles and genres) in the archive folder.

## Bipartite Graph
A 'regular' graph is a collection of nodes (points) connected by edges (lines). A bipartite graph splits nodes into two groups where edges only connect nodes from different groups and never within the same group.
In this project one group contains users, the other contains movies. An edge connects a user to a movie if that user rated that movie. For example, if User 1 rated "Toy Story" movie, there is an edge between User 1 and "Toy Story" movie. Users never connect to other users, and movies never connect to other movies.
This structure enables recommendations if User A and User B both rated the same movies, they are similar users. We can then recommend to User A movies that User B rated (but User A has not watched yet) by following paths through the graph.

## Recommender algorithms
- **Collaborative**: Finds users who watched the same movies as the selected user. It calculates similarity between the selected user and each similar user once per user pair using Jaccard (common movies divided by total unique movies both users watched). For each movie that the selected user has not watched, scores it by summing (similarity × rating) contributions. The similarity is between the selected user and a similar user, and rating is the similar user's rating of that specific unseen movie. Requires minimum 3 common movies between users to ensure quality matches. Then, it ranks all unseen movies by total score and recommends the top k.
- **Content-Based**: This is an extra feature. It vectorizes all movie titles using semantic embeddings (sentence-transformers with all-MiniLM-L6-v2 model). For each movie that the user has not watched, it calculates cosine similarity (range 0-1, unitless ratio) between that movie's title vector and the title vectors of movies the user watched, taking the maximum similarity. Filters for movies with similarity > 0.15, minimum 30 raters, and average rating ≥ 4.0. Then, it ranks unseen movies by similarity × rating score and recommends the top ones.
- **Same-Genre**: Based on the user's past movie genres to identify their category preferences. Filters for unseen movies sharing at least 2 common genres, minimum 30 raters, and average rating ≥ 3.8. Ranks by (rating × genre_count × popularity_boost) and recommends the top ones.
- **Cold-Start**: This is an extra feature. It scores movies by how many users rated them (most popular movies). Solves the cold-start problem for new users with no rating history. Note: Not evaluated because it doesn't personalize to user taste - there's no ground truth to compare against.

## Evaluations
The evaluation script `evaluate.py` measures the performance of three algorithms (Collaborative, Content-Based, Same-Genre) using an 80/20 split of the ratings data.

**How the split works:**
- **80% (training)**: Used to build the bipartite graph and data structures that recommenders use
- **20% (test)**: Hidden from recommenders to validate predictions

**What's hidden:** Specific user-movie connections (edges) from the test set are removed from the graph. For example, if User 5 rated Movie 123 in the test set, that edge is not in the training graph.

**What remains:** The movies and users themselves still exist in the graph through other ratings. Movie 123 might be in the graph because User 10 and User 20 rated it (their ratings are in the training set). User 5 is also in the graph with their other movies from the training set.

**Prediction:** The recommender uses patterns from other users (who have Movie 123 in their training ratings) to predict and recommend Movie 123 to User 5. Success is measured by checking if Movie 123 appears in User 5's hidden test ratings.

**Note**: Cold-Start is not evaluated because it recommends by popularity only (no personalization), so there's no ground truth to compare against user-specific test sets.

### Evaluation Metrics
- **Precision@K**: The percentage of recommended movies that were actually watched by the user in the test set.
- **Recall@K**: The percentage of the user's actual test-set movies that were successfully found in the recommendations.
- **F1@K**: The harmonic mean of Precision and Recall.
- **Hit Rate**: The percentage of users for whom at least one recommended movie was a correct prediction.

### Running Evaluations
Evaluations can be run in two ways:
1. **In-Browser**: Navigate to the **"Evaluations"** tab in the Streamlit UI, select the number of users and K value, and click **"Evaluate"**.
2. **Terminal**: Run the evaluation script (configured to sample 10 users for speed):
```bash
source venv/bin/activate && python evaluate.py
```

## Frontend

The frontend is built using Streamlit and is organized into two tabs:
1. **Recommendations**: The main interface where users can select a user ID and recommendation algorithm. It displays the top-k movie recommendations and a bipartite graph for the collaborative filtering algorithm.
2. **Evaluations**: An interface for running performance tests and viewing the results in a table.

## How to use UI
**Tabs:**
- **Recommendations**: The main page for getting personalized movie suggestions.
- **Evaluations**: The page for testing algorithm performance.

**Recommendations Tab Dropdowns:**
- **Select User ID**: Choose user to get recommendations for
- **Recommender**: Select recommendation algorithm (Collaborative, Content-Based, Same-Genre, Cold-Start). Only the collaborative (bipartite) algorithm will have the graph displayed.

**Recommendations:** Top k movies with relevance scores will appear. Higher scores indicate better matches, and they appear at the beginning of the list.

**Graph:** Visualizes recommendation paths for the collaborative algorithm (not for others as they are not based on graphs).
- Red = selected user
- Light blue = similar users
- Green = recommended movies

**Evaluations Tab:**
- **Users to test**: Select how many users from the test set to evaluate (max 100).
- **K value**: Select the size of the recommendation list for testing (max 30).
- **Evaluate Button**: Triggers the evaluation process (takes ~1-2 minutes).


## Three Unique Features
1. **Cold-Start Handling**: Recommends popular movies to new users who have no rating history, solving the cold-start problem where collaborative filtering fails. Not evaluated because it doesn't personalize to user taste.

2. **Content-Based Filtering**: Uses semantic embeddings and cosine similarity on movie titles to find semantically similar movies based on title content, independent of user ratings. Semantic embeddings can recognize synonyms (e.g., "phone" and "mobile") unlike lexical methods. Combines similarity scores with movie quality (ratings) for better recommendations.

3. **Same-Genre Recommendations**: Filters recommendations to movies sharing genres with the user's watched movies, then ranks by average rating weighted by genre overlap and popularity to ensure quality matches within preferred genres.

## Known Limitations

- **User dropdown limitation**: The user selection dropdown is limited to MAX_USERS (default: 50) to keep the interface manageable, meaning larger datasets will be truncated (see config.py).
- **Collaborative filtering dependency**: Collaborative filtering requires users to have watched common movies with other users; users with no overlapping movie history will receive poor or no recommendations.
- **Content-based scope**: The content-based recommender only uses movie titles for similarity calculations, ignoring other metadata (dataset constraint).
- **Graph visualization**: Graph visualization is only available for the collaborative filtering algorithm; other recommendation algorithms do not have movie-user relationships.
- **In-memory processing**: All data structures are loaded into memory, which may limit scalability for large datasets.
- **Strict filtering for precision**: Algorithms use aggressive quality filters (minimum raters, rating thresholds) which improve precision but may limit recommendation diversity.

## Next Steps

Future improvements for the recommendation system:
- **Scaling improvements**: Migrate from in-memory data structures to persistent databases to improve performance with large datasets.
- **Algorithm enhancements**: Explore advanced techniques such as matrix factorization (e.g. SVD), hybrid recommendation approaches combining multiple algorithms, and deep learning-based methods for better personalization.
- **Feature enhancements**: Integrate user feedback mechanisms, support real-time rating updates, expand content-based filtering to include movie descriptions and metadata, and implement A/B testing for algorithm comparison.
- **Performance optimizations**: Optimize graph traversal algorithms, implement parallel processing for similarity calculations, and add incremental updates to avoid full recomputation when new ratings are added.

## Contact

For questions or collaboration, please reach out to:

- **Almir Mustafic** — [GitHub](https://github.com/AlmirMBH)

## License

This project is licensed under the MIT License.

## Acknowledgments

This project uses the following third-party libraries, datasets, and services:

- **MovieLens Dataset**: The datasets used in this project are from [MovieLens Latest Small Dataset](https://www.kaggle.com/datasets/grouplens/movielens-latest-small) by GroupLens Research, licensed under the Creative Commons Attribution 4.0 International License.
- **pandas**: BSD License
- **Streamlit**: Apache License 2.0
- **matplotlib**: Matplotlib License (BSD-compatible)
- **NetworkX**: BSD License
- **scikit-learn**: BSD License

Special thanks to Professor Sead Delic for guidance and supervision during the course.

## Disclaimer

The MovieLens dataset used in this project is for educational and demonstration purposes only. This project is an academic exercise completed as part of the Algorithms and Data Structures II course and does not represent a production-ready recommendation system.
