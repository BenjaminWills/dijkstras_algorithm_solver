import networkx as nx
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from dijkstras_algorithm.dijkstra import Network


class GraphWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initialise graph
        self.distance_matrix = np.array(
            [
                [0.0, 4.0, 0.0, 2.0, 0.0],
                [0.0, 0.0, 5.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 3.0],
                [0.0, 1.0, 0.0, 0.0, 6.0],
                [0.0, 0.0, 0.0, 0.0, 0.0],
            ]
        )
        node_names = list("ABCDE")
        # Initialise network
        # self.network = Network(distance_matrix, node_names)

        # Create a figure for matplotlib
        self.figure = Figure(figsize=(5, 5))

        # Create a canvas for the figure
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # Draw the graph on the canvas
        self.draw_graph()

    def draw_graph(self):
        # Clear the figure
        self.figure.clf()

        # Draw the NetworkX graph on the figure
        # self.network.highlight_fastest_path("A", "B", ax=self.figure.add_subplot(111))
        graph = nx.DiGraph(self.distance_matrix)  # Update the canvas
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, ax=self.figure.add_subplot(111))
        self.canvas.draw()


if __name__ == "__main__":
    # Create the main window
    window = GraphWindow()
    window.mainloop()
