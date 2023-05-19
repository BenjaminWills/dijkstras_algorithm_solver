import numpy as np
import copy
import networkx as nx
import matplotlib.pyplot as plt


from typing import List


class Network:
    def __init__(
        self, adjacency_matrix: np.array, node_names: List[str] = None
    ) -> None:
        self.adjacency_matrix = adjacency_matrix
        self.num_nodes = adjacency_matrix.shape[0]
        self.node_names = node_names or range(self.num_nodes)

    def get_shortest_distances(self, node: int) -> dict[object, float]:
        """Uses Dijkstras algorithm to find the shortest distances to all of the nodes

        Parameters
        ----------
        node : int
            Starting node

        Returns
        -------
        dict[object,float]
            A dictionary who's keys are the node names and who's values are the distance of the selected node
            to the respective node.
        """
        unvisited_nodes = {n: 1 for n in range(0, self.num_nodes)}
        visited_nodes = {n: 0 for n in range(0, self.num_nodes)}
        routes = {n: [node] for n in range(0, self.num_nodes)}

        # Visit source node
        unvisited_nodes[node] = 0
        visited_nodes[node] = 1

        last_visited = node

        # Get initial distance matrix
        distance_matrix = self.init_distance_matrix(node)
        # Start loop
        while self.still_nodes_to_visit(unvisited_nodes):
            # Find nearest neighbours to the most recent visited node
            # Deep copy to avoid scoping issues
            nearest_neighbours = copy.deepcopy(self.adjacency_matrix[last_visited, :])
            nearest_neighbour, nearest_neighbour_distance = self.get_nearest_neighbour(
                nearest_neighbours, last_visited
            )

            nearest_neighbours = copy.deepcopy(self.adjacency_matrix[last_visited, :])

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

            unvisited_nodes[nearest_neighbour] = 0
            visited_nodes[nearest_neighbour] = 1

            # print(last_visited, nearest_neighbour)
            if last_visited != node:
                routes[last_visited].append(nearest_neighbour)

            last_visited = nearest_neighbour

        formatted_distance_matrix = {
            node_name: distance
            for node_name, distance in zip(self.node_names, distance_matrix)
        }
        # print(routes)
        return formatted_distance_matrix

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

    def get_nearest_neighbour(
        self, nearest_neighbours: np.array, last_visited_node: int
    ) -> tuple[float]:
        """Gets the nearest neighbour to a vertex

        Parameters
        ----------
        last_visited_node : int
            The index of the previously visited node

        Returns
        -------
        tuple[float]
            A tuple that is the index of the nearested neighbour node and the distance from the previous
            node.
        """
        maximus = nearest_neighbours.max()
        nearest_neighbours[nearest_neighbours == 0] = (
            maximus + 1
        )  # Avoiding issue of 0 values
        nearest_neighbour, nearest_neighbour_distance = (
            nearest_neighbours.argmin(),  # Nearest neighbour node name
            nearest_neighbours.min(),  # Nearest neighbout distance
        )
        return (nearest_neighbour, nearest_neighbour_distance)

    def draw_graph(self):
        """
        Draws the graph with the weights and the node names
        """
        graph = nx.DiGraph(self.adjacency_matrix)
        graph = nx.relabel_nodes(
            graph, {n: name for n, name in zip(range(self.num_nodes), self.node_names)}
        )
        pos = nx.spring_layout(graph)  # pos = nx.nx_agraph.graphviz_layout(G)
        nx.draw_networkx(graph, pos)
        labels = nx.get_edge_attributes(graph, "weight")
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
        plt.show()


if __name__ == "__main__":
    adjacency_matrix = np.array(
        [[0, 3, 0, 1], [0, 0, 1, 0], [0, 0, 0, 0], [0, 1, 2, 0]]
    )
    node_names = list("ABCD")
    network = Network(adjacency_matrix, node_names)
    print(network.get_shortest_distances(0))
