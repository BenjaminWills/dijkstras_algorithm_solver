import networkx as nx
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Create a NetworkX graph
        self.graph = nx.Graph()
        self.graph.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1)])

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
        nx.draw(self.graph, with_labels=True, ax=self.figure.add_subplot(111))

        # Update the canvas
        self.canvas.draw()


if __name__ == "__main__":
    # Create the main window
    window = GraphWindow()
    window.mainloop()
