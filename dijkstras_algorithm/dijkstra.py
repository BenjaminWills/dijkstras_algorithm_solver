import numpy as np
import copy

from typing import List


class Network:
    def __init__(
        self, adjacency_matrix: np.array, node_names: List[str] = None
    ) -> None:
        self.adjacency_matrix = adjacency_matrix
        self.num_nodes = adjacency_matrix.shape[0]
        self.node_names = node_names or range(self.num_nodes)

    def get_shortest_distances(self, node: int) -> np.array:
        """Uses Dijkstras algorithm to find the shortest distances to all of the nodes

        Parameters
        ----------
        node : int
            Starting node

        Returns
        -------
        np.array
            An array whose elements correspond to the shortest distance the node with that index
        """
        unvisited_nodes = {n: 1 for n in range(0, self.num_nodes)}
        visited_nodes = {n: 0 for n in range(0, self.num_nodes)}

        # Visit source node
        unvisited_nodes[node] = 0
        visited_nodes[node] = 1

        last_visited = node

        # Get initial distance matrix
        distance_matrix = self.init_distance_matrix(node)
        # Start loop
        while self.still_nodes_to_visit(unvisited_nodes):
            # Find nearest neighbours to the most recent visited node
            nearest_neighbours = copy.deepcopy(
                self.adjacency_matrix[last_visited, :]
            )  # Deep copy to avoid scoping issues

            maximus = nearest_neighbours.max()
            nearest_neighbours[nearest_neighbours == 0] = (
                maximus + 1
            )  # Avoiding issue of 0 values
            nearest_neighbour, nearest_neighbour_distance = (
                nearest_neighbours.argmin(),  # Nearest neighbour node name
                nearest_neighbours.min(),  # Nearest neighbout distance
            )

            new_distance = distance_matrix[last_visited] + nearest_neighbour_distance

            if distance_matrix[nearest_neighbour] > new_distance:
                distance_matrix[nearest_neighbour] = new_distance

            unvisited_nodes[nearest_neighbour] = 0
            visited_nodes[nearest_neighbour] = 1
            last_visited = nearest_neighbour
        return distance_matrix

    def init_distance_matrix(self, source_node: int) -> np.array:
        # Initialise distance matrix
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


if __name__ == "__main__":
    adjacency_matrix = np.array(
        [[0, 3, 0, 1], [0, 0, 1, 0], [0, 0, 0, 0], [0, 1, 2, 0]]
    )
    network = Network(adjacency_matrix)
    print(network.get_shortest_distances(0))
