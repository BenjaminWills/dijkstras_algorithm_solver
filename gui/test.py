import networkx as nx
import tkinter as tk
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

        # Clear the matrix frame
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        # Create an entry box for each matrix element
        self.matrix_entries = []
        for i in range(self.num_nodes):
            row_entries = []
            for j in range(self.num_nodes):
                entry = tk.Entry(self.matrix_frame, width=5)
                entry.grid(row=i, column=j)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

    def create_graph(self):
        # Get the matrix elements from the entry boxes
        distances = []
        for i in range(self.num_nodes):
            row_distances = []
            for j in range(self.num_nodes):
                distance = int(self.matrix_entries[i][j].get())
                row_distances.append(distance)
            distances.append(row_distances)

        # Set the matrix elements as edge weights in the graph
        self.graph.clear()
        self.graph.add_weighted_edges_from(
            [
                (i, j, distances[i][j])
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
