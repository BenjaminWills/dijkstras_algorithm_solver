import networkx as nx
import tkinter as tk
import numpy as np
import string

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Number of nodes
        self.num_nodes = 0

        # Create a NetworkX graph
        self.graph = nx.Graph()

        # Create a figure for matplotlib
        self.figure = Figure(figsize=(5, 5))

        # Create a canvas for the figure
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # Create a frame for node count input
        input_frame = tk.Frame(self)
        input_frame.pack()

        # Create a label and entry for node count
        node_label = tk.Label(input_frame, text="Number of Nodes:")
        node_label.pack(side=tk.LEFT)
        self.node_entry = tk.Entry(input_frame)
        self.node_entry.pack(side=tk.LEFT)
        button = tk.Button(
            input_frame, text="Create Matrix", command=self.create_matrix
        )
        button.pack(side=tk.LEFT)

        # Create a frame for the matrix input
        self.matrix_frame = tk.Frame(self)
        self.matrix_frame.pack()

        # Create a button to create the graph
        button = tk.Button(self, text="Create Graph", command=self.create_graph)
        button.pack()

    def create_matrix(self):
        # Get the number of nodes from the entry box
        self.num_nodes = int(self.node_entry.get())

        # Label the nodes after letters rather than numbers
        self.node_label_map = {
            node_id: node_name
            for node_id, node_name in zip(
                range(self.num_nodes), string.ascii_uppercase[: self.num_nodes]
            )
        }

        # Clear the matrix frame
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        # Create labels for row/column headers
        for i in range(self.num_nodes):
            row_label = tk.Label(self.matrix_frame, text=self.node_label_map[i])
            row_label.grid(row=i + 1, column=0, sticky=tk.W)
            col_label = tk.Label(self.matrix_frame, text=self.node_label_map[i])
            col_label.grid(row=0, column=i + 1, sticky=tk.N)

        # Create an entry box for each matrix element
        self.matrix_entries = []
        for i in range(self.num_nodes):
            row_entries = []
            for j in range(self.num_nodes):
                entry = tk.Entry(self.matrix_frame, width=5)
                entry.grid(row=i + 1, column=j + 1)
                entry.insert(tk.END, 0)  # Set the default value to 0
                row_entries.append(entry.get())
            self.matrix_entries.append(row_entries)
        self.distance_matrix = np.array(self.matrix_entries)

    def create_graph(self):
        # Set the matrix elements as edge weights in the graph
        self.graph.clear()
        self.graph.add_weighted_edges_from(
            [
                (i, j, self.matrix_entries[i][j])
                for i in range(self.num_nodes)
                for j in range(self.num_nodes)
            ]
        )

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
