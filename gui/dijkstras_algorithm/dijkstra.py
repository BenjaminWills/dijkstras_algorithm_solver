import copy
from typing import Dict, List, Union

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from tqdm import tqdm

ROUTES = Dict[
    str, Dict[str, Union[List[str], float]]
]  # Definition of the route dictionary, has keys corresponding to the distance and the route to that node

NODE_NAME = Union[str, int, object]  # The datatypes that can represent a node name


class Network:
    def __init__(
        self, adjacency_matrix: np.array, node_names: List[str] = None
    ) -> None:
        self.adjacency_matrix = adjacency_matrix
        self.num_nodes = adjacency_matrix.shape[0]
        self.node_names = node_names or range(self.num_nodes)

    def get_shortest_distances(self, node_name: str) -> ROUTES:
        """Uses Dijkstras algorithm to find the shortest distances to all of the nodes

        Parameters
        ----------
        node : int
            Starting node

        Returns
        -------
        ROUTES:
            A dictionary containing information on the distance to a node and it's path
        """
        # Initialise progress bar
        pbar = tqdm(total=self.num_nodes)

        # Initialise nodes to visit
        unvisited_nodes = {n: 1 for n in range(0, self.num_nodes)}
        # Initialise route dictionary
        routes = {node_name: {"distance": 0, "route": [node_name]}}

        node = self.node_names.index(node_name)
        # Visit source node
        unvisited_nodes[node] = 0

        last_visited = node

        # Get initial distance matrix
        distance_matrix = self.init_distance_matrix(node)
        # Start loop
        while self.still_nodes_to_visit(unvisited_nodes):
            # Find nearest neighbours to the most recent visited node
            # Deep copy to avoid scoping issues

            nearest_neighbours = self.adjacency_matrix[last_visited, :]
            nearest_neighbour = self.get_nearest_neighbour(nearest_neighbours)

            # The issue is we need to update ALL of the distances as this new vertex could reveal
            # a shorter route, so we do a for loop through all the applicable neighbours
            for index, neighbour in enumerate(nearest_neighbours):
                # A neighbour is an index in which the distances > 0 (as this means there is a direct link)
                if neighbour:
                    # Define the new distance as the distance to the previous node plus that neighbour distance
                    # if this is less than the distance in the distance matrix, we have found a faster route
                    new_distance = distance_matrix[last_visited] + neighbour
                    if new_distance < distance_matrix[index]:
                        distance_matrix[index] = new_distance

                        nearest_neighbour_node_name = self.node_names[index]
                        last_visited_node_name = self.node_names[last_visited]
                        updated_route = routes[last_visited_node_name]["route"] + [
                            nearest_neighbour_node_name
                        ]

                        routes[nearest_neighbour_node_name] = {
                            "distance": distance_matrix[index],
                            "route": updated_route,
                        }

            unvisited_nodes[nearest_neighbour] = 0
            pbar.update(1)

            last_visited = nearest_neighbour
        pbar.update(1)
        return routes

    def init_distance_matrix(self, source_node: int) -> np.array:
        """Initialise n dimensional vector to hold distances from the starting node
        These will be arbritrarily large apart from the base node.

        Parameters
        ----------
        source_node : int
            The index of the source node

        Returns
        -------
        np.array
            An array consisting of infinities and one 0 at the index of the source node
        """
        distance_matrix = np.full(self.adjacency_matrix.shape[0], np.inf)
        distance_matrix[source_node] = 0
        return distance_matrix

    def still_nodes_to_visit(self, unvisited_nodes: dict[str, int]) -> bool:
        """Returns True if there are still nodes that have not been visited

        Parameters
        ----------
        unvisited_nodes : dict[str, int]
            A dictionary with keys being the indexes of the nodes and the value being 1 if the node
            has not been visited yet and 0 otherwise

        Returns
        -------
        bool
            True if there are still nodes that have not been visited, False otherwise
        """
        return list(unvisited_nodes.values()) != [0] * self.num_nodes

    def get_nearest_neighbour(self, nearest_neighbours: np.array) -> int:
        """Gets the nearest neighbour to a vertex

        Parameters
        ----------
        last_visited_node : int
            The index of the previously visited node

        Returns
        -------
        int
            The index of the nearest neighbour
        """
        nearest_neighbours_copy = copy.deepcopy(nearest_neighbours)
        maximus = nearest_neighbours_copy.max()
        nearest_neighbours_copy[nearest_neighbours_copy == 0] = (
            maximus + 1
        )  # We do this to stop nodes with no direct connecting edge being chosen
        nearest_neighbour = (
            nearest_neighbours_copy.argmin()
        )  # Nearest neighbour node name
        return nearest_neighbour

    def draw_graph(self, display: bool = False) -> nx.DiGraph:
        """
        Draws the graph with the weights and the node names
        """
        graph = nx.DiGraph(self.adjacency_matrix)
        graph = nx.relabel_nodes(
            graph,
            {
                node_index: node_name
                for node_index, node_name in zip(range(self.num_nodes), self.node_names)
            },
        )
        if display:
            pos = nx.spring_layout(graph)
            nx.draw_networkx(graph, pos)
            labels = nx.get_edge_attributes(graph, "weight")
            nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
            plt.show()
        return graph

    def highlight_fastest_path(
        self, from_node: NODE_NAME, to_node: NODE_NAME, ax=None, display: bool = False
    ) -> nx.DiGraph:
        """Highlights the fastest path from any two nodes on the graph

        Parameters
        ----------
        from_node : str
            Starting node name
        to_node : str
            Finishing node name
        """
        graph = nx.DiGraph(self.adjacency_matrix)
        graph = nx.relabel_nodes(
            graph, {n: name for n, name in zip(range(self.num_nodes), self.node_names)}
        )
        if display:
            routes = self.get_shortest_distances(from_node)
            path_route = routes[to_node]
            distance, node_list = path_route.values()
            pos = nx.spring_layout(graph)
            nx.draw_networkx(graph, pos)
            labels = nx.get_edge_attributes(graph, "weight")

            # Creating the edge colour map
            node_pairs = []
            num_route_nodes = len(node_list)
            for index in range(num_route_nodes):
                if index + 1 < num_route_nodes:
                    node_pairs.append((node_list[index], node_list[index + 1]))
            # This will give the list of all nodes to be coloured

            colour_map = []
            for edge in list(graph.edges):
                if edge in node_pairs:
                    colour_map.append("red")
                else:
                    colour_map.append("black")

            # Colouring edges
            nx.draw_networkx_edges(graph, pos, edge_color=colour_map, ax=ax)
            # Drawing the edge distance labels
            nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, ax=ax)
            # Display the output
            plt.show()
        return graph
