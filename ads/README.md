# Movie Recommendation System
Bipartite graph-based movie recommendation system with multiple recommendation strategies (python < 3.14 required).

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

## Stop Project
Stop: `pkill -f "streamlit run app.py"` or `Ctrl+C`

## Configuration File
The `config.py` file contains system settings. The number of users is pretty low to keep the graph readable (edges and nodes). The way the recommender works is customized in this file.
- **RATINGS_FILE**: Path to the ratings CSV file (default: `archive/ratings.csv`)
- **MOVIES_FILE**: Path to the movies CSV file (default: `archive/movies.csv`)
- **RECOMMENDATION_TOP_K**: Number of top recommendations to return (default: 10)
- **MAX_USERS**: Maximum number of users displayed in the user selection dropdown (default: 50)
- **MAX_SIMILAR_USERS**: Number of similar users to show per recommended movie in graph visualization is configurable to keep the visibility of the similar users in the graph. The algorithm prioritizes unique users first, then reuses users if needed.

After making any changes to `config.py`, press the "Rerun" button in the upper right corner of the Streamlit UI to apply and see the changes.


## Dataset
The datasets used in this project are from [MovieLens Latest Small Dataset](https://www.kaggle.com/datasets/grouplens/movielens-latest-small) from Kaggle. There are ratings.csv (user-movie ratings) and movies.csv (movie titles and genres) in the archive folder.

## Bipartite Graph
A 'regular' graph is a collection of nodes (points) connected by edges (lines). A bipartite graph splits nodes into two groups where edges only connect nodes from different groups and never within the same group.
In this project one group contains users, the other contains movies. An edge connects a user to a movie if that user rated that movie. For example, if User 1 rated "Toy Story" movie, there is an edge between User 1 and "Toy Story" movie. Users never connect to other users, and movies never connect to other movies.
This structure enables recommendations if User A and User B both rated the same movies, they are similar users. We can then recommend to User A movies that User B rated (but User A has not watched yet) by following paths through the graph.

## Recommender algorithms
- **Collaborative**: Finds users who watched the same movies as the selected user. It calculates similarity between the selected user and each similar user once per user pair using Jaccard (common movies divided by total unique movies both users watched). For each movie that the selected user has not watched, scores it by summing (similarity × rating) contributions. The similarity is between the selected user and a similar user, and rating is the similar user's rating of that specific unseen movie. Then, it ranks all unseen movies by total score and recommends the top k.
- **Content-Based**: This is an extra feature. It vectorizes all movie titles using TF-IDF. For each movie that the user has not watched, it calculates cosine similarity (range 0-1, unitless ratio) between that movie's title vector and the title vectors of movies the user watched, taking the maximum similarity. then, it ranks unseen movies by similarity score and recommends the top ones.
- **Same-Genre**: This is an extra feature. It scores movies by average rating, but only includes movies sharing genres with movies that a user watched.
- **Cold-Start**: This is an extra feature. It scores movies by how many users rated them (most popular movies).

## How to use UI
**Dropdowns:**
- **Select User ID**: Choose user to get recommendations for
- **Recommender**: Select recommendation algorithm (Collaborative, Content-Based, Same-Genre, Cold-Start). Only the collaborative (bipartite) algorithm will have the graph displayed.

**Recommendations:** Top k movies with relevance scores will appear. Higher scores indicate better matches, and they appear at the beginning of the list.

**Graph:** Visualizes recommendation paths for the collaborative algorithm (not for others as they are not based on graphs).
- Red = selected user
- Blue = similar users
- Green = recommended movies


## Three Unique Features (explained above)
1. **Cold-Start Handling**: Recommends popular movies to new users who have no rating history, solving the cold-start problem where collaborative filtering fails.

2. **Content-Based Filtering**: Uses TF-IDF vectorization and cosine similarity on movie titles to find semantically similar movies based on title content, independent of user ratings.

3. **Same-Genre Recommendations**: Filters recommendations to movies sharing genres with the user's watched movies, then ranks by average rating to ensure quality matches within preferred genres.
