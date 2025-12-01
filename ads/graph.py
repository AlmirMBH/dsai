import pandas as pd

class Node:
    def __init__(self, node_id, node_type):
        # Store the identifier for this node (user ID or movie ID).
        # Store the type of node 'user' or 'movie'.
        self.edges = []
        self.node_id = node_id
        self.node_type = node_type   
    
    
    def add_edge(self, edge):
        # Add an edge to this node's list of edges.
        # This connects the node to another node in the graph.
        self.edges.append(edge)
    

    def get_neighbors(self):
        # Fetch all nodes that are connected to this node via edges.
        neighbors = []
        
        # Go through each edge connected to this node.
        for edge in self.edges:
            # An edge connects two nodes: node1 and node2.
            # Find which node is the neighbor (the one that's not this node).
            if edge.node1 == self:
                # If this node is node1, then the neighbor is node2.
                neighbor = edge.node2
            else:
                # If this node is node2, then the neighbor is node1.
                neighbor = edge.node1
            
            # Add the neighbor to the list.
            neighbors.append(neighbor)
        
        return neighbors


class Edge:
    def __init__(self, node1, node2, weight=0):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight # Store the weight of the edge (e.g., rating value), default 0.


class BipartiteGraph:
    def __init__(self, ratings_file):
        # Load ratings data from CSV file (see archive/ratings.csv), user-movie interactions with ratings.
        ratings = pd.read_csv(ratings_file)
        self.nodes = {}
        self.edges = []
        
        # Process each rating row to build the graph.
        # Extract user ID from the row and convert to integer.
        # Extract movie ID from the row and convert to integer.
        # Extract rating value from the row and convert to float.
        for i, row in ratings.iterrows():
            user_id = int(row['userId'])
            movie_id = int(row['movieId'])
            rating = float(row['rating'])
            
            # Create user node if it does not exist.
            # Store it in the nodes dictionary.
            if user_id not in self.nodes:
                user_node = Node(user_id, 'user')
                self.nodes[user_id] = user_node
            
            # Create movie node if it does not exist yet.
            # Store it in the nodes dictionary.
            if movie_id not in self.nodes:
                movie_node = Node(movie_id, 'movie')
                self.nodes[movie_id] = movie_node
            
            # Get the user and movie nodes we just created or found.
            user_node = self.nodes[user_id]
            movie_node = self.nodes[movie_id]
            
            # Create an edge between the user to the movie.
            # The edge weight is the rating the user gave to the movie.
            # Add this edge to the graph's list of all edges.
            edge = Edge(user_node, movie_node, rating)
            self.edges.append(edge)
            
            # Add the edge to the user node's list of edges.
            # The user node knows it is connected to this movie.
            user_node.add_edge(edge)
            
            # Add the edge to the movie node's list of edges.
            # Thhe movie node knows it is connected to this user.
            movie_node.add_edge(edge)
    
    
    def get_user_movies(self, user_id):
        movies = set()

        # Fetch if the user exists in the graph, or return an empty set.
        if user_id not in self.nodes:
            return set()
        
        # Fetch the user node from the nodes dictionary.
        user_node = self.nodes[user_id]        
        
        # Go through all edges connected to this user node.
        for edge in user_node.edges:
            # Find which node is connected to the user through this edge.
            # An edge has two nodes: node1 and node2.
            if edge.node1 == user_node:
                # If the user is node1, then the connected node is node2.
                neighbor = edge.node2
            else:
                # If the user is node2, then the connected node is node1.
                neighbor = edge.node1
            
            # Check if the neighbor is a movie (not another user).
            # Users only connect to movies (bipartite graph).
            if neighbor.node_type == 'movie':
                # Add the movie ID to our set of movies.
                movies.add(neighbor.node_id)
        
        return movies
    

    def get_movie_users(self, movie_id):
        users = set()

        # Check if the movie exists in the graph.
        # If the movie does not exist, return an empty set.
        if movie_id not in self.nodes:
            return set()
        
        # Get the movie node from our nodes dictionary.
        movie_node = self.nodes[movie_id]        
        
        # Go through all edges connected to this movie node.
        for edge in movie_node.edges:
            # Find which node is connected to the movie through this edge.
            # An edge has two nodes: node1 and node2.
            if edge.node1 == movie_node:
                # If the movie is node1, then the connected node is node2.
                neighbor = edge.node2
            else:
                # If the movie is node2, then the connected node is node1.
                neighbor = edge.node1
            
            # Check if the neighbor is a user (not another movie).
            # Movies only connect to users (bipartite graph).
            if neighbor.node_type == 'user':
                # Add the user ID to the set of users.
                users.add(neighbor.node_id)
        
        return users
    

    def get_rating(self, user_id, movie_id):
        # Check if both the user and movie exist in the graph.
        # If either does not, return rating 0.
        if user_id not in self.nodes or movie_id not in self.nodes:
            return 0
        
        # Get the user and movie nodes from the nodes dictionary.
        user_node = self.nodes[user_id]
        movie_node = self.nodes[movie_id]
        
        # Go through all edges connected to the user node.
        # We're looking for the edge that connects this user to this specific movie.
        for edge in user_node.edges:
            # Find which node is connected to the user through this edge.
            if edge.node1 == user_node:
                # If the user is node1, then the connected node is node2.
                neighbor = edge.node2
            else:
                # If the user is node2, then the connected node is node1.
                neighbor = edge.node1
            
            # Check if this edge connects to the movie we're looking for.
            if neighbor == movie_node:
                # Found the edge! Return its weight (the rating).
                return edge.weight
        
        # If we didn't find an edge connecting this user to this movie,
        # return rating 0 (user hasn't rated this movie).
        return 0
    

    def get_user_movies_dict(self):
        result = {}

        # Create a dictionary mapping each user ID to the set of movies they watched.
        # Initialize an empty dictionary to store the result.
        # Go through all nodes in the graph.
        for node_id, node in self.nodes.items():
            # Only process user nodes (skip movie nodes).
            if node.node_type == 'user':
                # Get all movies watched by this user.
                movies_watched = self.get_user_movies(node_id)
                # Store the mapping: user_id -> set of movie_ids.
                result[node_id] = movies_watched
        
        return result
    

    def get_movie_users_dict(self):
        result = {}

        # Create a dictionary mapping each movie ID to the set of users who watched it.
        # Initialize an empty dictionary to store the result.        
        # Go through all nodes in the graph.
        for node_id, node in self.nodes.items():
            # Only process movie nodes (skip user nodes).
            if node.node_type == 'movie':
                # Get all users who watched this movie.
                users_who_watched = self.get_movie_users(node_id)
                # Store the mapping: movie_id -> set of user_ids.
                result[node_id] = users_who_watched
        
        return result

