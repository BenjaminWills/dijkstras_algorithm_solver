# Importing from within another directory
import sys

path_to_dijkstra_file = "../dijkstras_algorithm_solver"

sys.path.insert(0, path_to_dijkstra_file)

import string
import tkinter as tk
from tkinter import ttk

import networkx as nx
import numpy as np
from dijkstra import Network
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class GraphWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Number of nodes
        self.num_nodes = 0

        # Create a NetworkX graph
        self.graph = nx.Graph()

        # Create a figure for matplotlib
        self.figure = Figure(figsize=(6, 6))

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
        self.node_names = list(string.ascii_uppercase[: self.num_nodes])
        self.node_label_map = {
            node_id: node_name
            for node_id, node_name in zip(range(self.num_nodes), self.node_names)
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
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

        # Create a label and dropdown for the source node
        source_label_col = 1
        source_label_row = self.num_nodes + 1

        source_label = ttk.Label(self.matrix_frame, text="Source Node:")
        source_label.grid(row=source_label_row, column=source_label_col, padx=5, pady=0)
        self.source_var = tk.StringVar()
        self.source_dropdown = ttk.Combobox(
            self.matrix_frame,
            textvariable=self.source_var,
        )
        self.source_dropdown.bind("<<ComboboxSelected>>", self.update_dropdown)
        self.source_dropdown.grid(
            row=source_label_row, column=source_label_col + 1, padx=5, pady=0
        )

        # Create a label and dropdown for the target node
        target_label_col = 1
        target_label_row = self.num_nodes + 2

        target_label = ttk.Label(self.matrix_frame, text="Target Node:")
        target_label.grid(row=target_label_row, column=target_label_col, padx=5, pady=5)
        self.target_var = tk.StringVar()
        self.target_dropdown = ttk.Combobox(
            self.matrix_frame, textvariable=self.target_var
        )
        self.target_dropdown.grid(
            row=target_label_row, column=target_label_col + 1, padx=5, pady=5
        )
        self.source_dropdown["values"] = self.node_names
        self.target_dropdown.bind("<<ComboboxSelected>>", self.draw_fastest_path)

    def update_dropdown(self, placeholder) -> None:
        source_node = self.source_var.get()
        self.routes = self.network.get_shortest_distances(source_node)
        self.target_dropdown["values"] = list(self.routes.keys())

    def create_graph(self):
        distance_list = []
        for i in range(self.num_nodes):
            row = []
            for j in range(self.num_nodes):
                row.append(int(self.matrix_entries[i][j].get()))
            distance_list.append(row)

        self.distance_matrix = np.array(distance_list)

        # Set the matrix elements as edge weights in the graph
        self.graph.clear()
        self.network = Network(self.distance_matrix, self.node_names)
        self.graph = self.network.draw_graph()

        # Draw the graph on the canvas
        self.draw_graph()

    def draw_graph(self):
        # Clear the figure
        self.figure.clf()

        # Get weight labels
        labels = nx.get_edge_attributes(self.graph, "weight")
        # Draw the NetworkX graph on the figure
        self.pos = nx.spring_layout(self.graph, weight="length")
        nx.draw(
            self.graph,
            self.pos,
            with_labels=True,
            ax=self.figure.add_subplot(111),
        )
        # Update the canvas
        self.canvas.draw()

    def draw_fastest_path(self, placeholder):
        # Clear the figure
        self.figure.clf()

        # Get the selected source and target nodes
        target_node = self.target_var.get()

        # Perform the fastest path calculation
        path_route = self.routes[target_node]
        distance, node_list = path_route.values()

        # Creating the edge colour map
        node_pairs = []
        num_route_nodes = len(node_list)
        for index in range(num_route_nodes):
            if index + 1 < num_route_nodes:
                node_pairs.append((node_list[index], node_list[index + 1]))
        # This will give the list of all nodes to be coloured

        colour_map = []
        for edge in list(self.graph.edges):
            if edge in node_pairs:
                colour_map.append("red")
            else:
                colour_map.append("black")

        # Draw the network
        nx.draw(
            self.graph,
            self.pos,
            with_labels=True,
            edge_color=colour_map,
            ax=self.figure.add_subplot(111),
        )
        # Drawing the edge distance labels
        # NOTE: does not seem to work with TKinter :'( Not too sure why as it is just displaying an image.
        # nx.draw_networkx_edge_labels(
        #     self.graph, self.pos, edge_labels=labels, ax=self.figure.add_subplot(111)
        # )
        # Display the output
        # Update the canvas
        self.canvas.draw()


if __name__ == "__main__":
    # Create the main window
    window = GraphWindow()
    window.title("Dijkstra solver")
    window.mainloop()
