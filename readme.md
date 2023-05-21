# Dijkstra's algorithm visualiser

This is just a fun tool to visualise how Dijkstra`s algorithm works.

## The algorithm

Dijkstra's algorithm allows us to find the shortest distance between any two nodes on a graph. But how does it work?

### What is a directed graph?

A `directed graph` is simply a graph with `edges` connecting `nodes` that can be one way, meaning that you can traverse along them towards a node but not back. This can lead to some interesting problems, an example of a directed graph is below:

<div style="text-align: center;">
  <img src="./images/graph.png" alt="Graph" />
  <p style="text-align: center;">A directed graph with 5 nodes.</p>
</div>

We can see here that we can traverse from node `A` to node `B` but not from node `B` to node `A`!

### Direction matrices

We can denote a graph mathematically using a `direction matrix`:

<div style="text-align: center;">
  <img src="images/distance_matrix.png" alt="Graph" />
  <p style="text-align: center;">The above graph's corresponding distance matrix</p>
</div>

The way to interperet this is seeing the y axis as being the `node from` and the x axis as being the `node to`, so for example if we want to know the distance going from node `A` to node `B`, we look for `A` vertically and `B` horizontally, these align on `4` showing that the distance between them is 4, for a sanity check we can compare to the diagram, and it's correct!

### Dijkstra's algorithm

Now we can tackle the beast that is `Dijkstra's algorithm`. Here are the steps:

1. Choose a starting node, create a list of distances of nodes from that starting node, each element apart from the element that represents this node should be set to ∞, so it should look like [∞,∞,∞,...,0,...,∞], also create a list of unvisited nodes to keep track which nodes you have visited.
2. Find all nodes that are `neighbours` of your node, meaning that they connect via an `edge`, for each edge found calculate the new distance to that node, if this distance is less than the distance stored in the distance list, replace that larger distance with this smaller one.
3. Move to the nearest neighbour to the previous node and repeat step 2. Terminate the algorithm if all nodes have been visited, i.e when your list of unvisited nodes is empty.

#### Worked example

Suppose that we're looking at the graph from before: 

<div style="text-align: center;">
  <img src="./images/graph.png" alt="Graph" />
  <p style="text-align: center;">A directed graph with 5 nodes.</p>
</div>

To begin the algorithm lets make a list of unvisited nodes: $[A,B,C,D,E]$, now lets choose A as our `root node`, i.e we will find the shortest distance to all nodes from `A`. Let us initialise our distance list too: $[0,∞,∞,∞,∞]$

The neighbours of `A` are `B` and `D`, the nearest neighbour to A is `D` and therefore we select `D` as our next node. Before we do this we need to update our distance list: $[0,4,∞,2,∞]$.

Now starting from `D`, our neighbours are `B` and `E`, the nearest of these is `B` which will be our next node. Before moving on we update the distance list to check if going through `D` leads to shorter distances: $[0,3,∞,2,8]$. Note 2 things here:

1. The distance from `A` to `B` has changed from 4 to 3, this is because going from `A->D->B` is less costly than going from `A->B` directly! Hence we must change the entry in the distance list.
2. The distance from `A` to `E` is 8, this is because we must first go to `D` and then to `E`, `A->D->E`, this leads to 2 + 6 = 8.

Now we are at node `B`, `B` only connects to `C` and hence `C` is the nearest neighbour and will be the next node. Updating the distance list: $[0,3,8,2,8]$.

Now `C` only connects to `E`, thus it shall be our next node. Updating the distance matrix at `C` we get: $[0,3,8,2,8]$.

`E` connects to nothing so our algorithm is completed. Leaving us with the following distance list: $[0,3,8,2,8]$!

So now we know:

- `A->B` $= 3$
- `A->C` $= 8$
- `A->D` $= 2$
- `A->E` $= 8$

And we found this using Dijkstra's algorithm!

### Time complexity

You may be asking why it would be worth it to use `Dijkstra's algorithm`, we use it due to its `logarithmic` time complexity, meaning that it performs very well for large graphs, the order of the algorithm is actually:

$$O(E\log(V))$$

Where $E$ is the total number of edges and $V$ is the total number of nodes.

This means that for each edge added the time to run the algorithm increases multiplicatively and for each node added the time increases logarithmically.

Note that the proper way to make this algorithm efficient is to use C++ or some other `lower level` language than python!

## The GUI

Run the `GUI` using:

```sh
make start_gui
```

The aim of this gui is to be able to play around with the shortest path algorithm.

![dijkstra_showcase](https://github.com/BenjaminWills/dijkstras_algorithm_solver/assets/90726430/c5ce422f-2b3b-4851-9a50-0bb489174298)

## Non GUI use

Check out the example by running the

```sh
make open_example
```

command, this is a notebook that goes through what the module can do.
