class Node:
    def __init__(self, node_id, node_type):
        self.edges = []
        self.node_id = node_id
        self.node_type = node_type
    
    
    def add_edge(self, edge):
        self.edges.append(edge)
    

    def get_neighbor_nodes(self):
        # Call on a node to get all nodes that are connected to it via its edges.
        neighbors = []
        
        for edge in self.edges:
            if edge.node1 == self:
                neighbor = edge.node2
            else:
                neighbor = edge.node1
            neighbors.append(neighbor)
        
        return neighbors


class Edge:
    def __init__(self, node1, node2, weight=0):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight


class BipartiteGraph:
    """
    Bipartite graph represent user-movie relationships and edges represent ratings.
    """
    def __init__(self, ratings_df):
        self.user_nodes = {}
        self.movie_nodes = {}
        
        # Extract user ID, movie ID, and rating from dataframe and build the graph.
        for i, row in ratings_df.iterrows():
            user_id = int(row['userId'])
            movie_id = int(row['movieId'])
            rating = float(row['rating'])
            
            # If it does not exist, create a new user in the user_nodes dictionary.
            if user_id not in self.user_nodes:
                user_node = Node(user_id, 'user')
                self.user_nodes[user_id] = user_node
            
            # If it does not exist, create a new movie in the movie_nodes dictionary.
            if movie_id not in self.movie_nodes:
                movie_node = Node(movie_id, 'movie')
                self.movie_nodes[movie_id] = movie_node
        
            user_node = self.user_nodes[user_id]
            movie_node = self.movie_nodes[movie_id]
            
            # Edge between the user and the movie (weight is user's movie rating).
            edge = Edge(user_node, movie_node, rating)
            user_node.add_edge(edge)
            movie_node.add_edge(edge)
    
    
    def get_user_movies(self, user_id):
        """Return set of movie IDs that the user has watched."""
        if user_id not in self.user_nodes:
            return set()
        
        movies = set()
        user_node = self.user_nodes[user_id]
        neighbors = user_node.get_neighbor_nodes()
        
        for neighbor in neighbors:
            movies.add(neighbor.node_id)

        return movies
    

    def get_movie_users(self, movie_id):
        """Return set of user IDs who have watched the movie."""
        if movie_id not in self.movie_nodes:
            return set()
        
        users = set()
        movie_node = self.movie_nodes[movie_id]
        neighbors = movie_node.get_neighbor_nodes()
        
        for neighbor in neighbors:
            users.add(neighbor.node_id)

        return users
    

    def get_rating(self, user_id, movie_id):
        """Return the rating for a user-movie pair, or 0 if not rated."""
        if user_id not in self.user_nodes or movie_id not in self.movie_nodes:
            return 0
        
        rating = 0
        user_node = self.user_nodes[user_id]
        movie_node = self.movie_nodes[movie_id]
        
        # Iterate over the user's edges and find the edge that
        # connects the user to this movie (node1 or node2).
        for edge in user_node.edges:
            if edge.node1 == user_node:
                neighbor = edge.node2
            else:
                neighbor = edge.node1
            
            if neighbor == movie_node:
                rating = edge.weight
        
        return rating
    

    def get_user_ids(self):
        # User IDs for the dropdown menu.
        return list(self.user_nodes.keys())
    

    def get_movie_ids(self):
        # Movie IDs for the dropdown menu.
        return list(self.movie_nodes.keys())

