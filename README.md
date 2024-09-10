# Dijkstra's Algorithm Implementation in Python

This repository contains a Python implementation of Dijkstra's Algorithm for finding the shortest path between two nodes in a graph. The algorithm uses a sparse travel time matrix and a node dictionary that contains coordinates, inlinks, and outlinks for each node.

## Features

- Finds the shortest path between two nodes in a graph.
- Handles sparse travel time matrices efficiently.
- Returns the shortest time, the path taken, and the list of path links.

## Requirements

This code requires the following Python libraries:

- `numpy`
- `itertools` (included in Python's standard library)

To install `numpy`, run:
```bash
pip install numpy
```

## How to Use

To use this Dijkstra's algorithm, simply import the `dijkstra` function in your Python project and provide the necessary parameters: starting node, ending node, list of nodes, sparse travel time matrix, and a dictionary of node information (including coordinates, inlinks, and outlinks).

### Parameters

- **start (int)**: The starting node ID.
- **end (int)**: The target node ID where the path ends.
- **list_nodes (list)**: A list of all node IDs in the graph.
- **orig_sparse_travel_time_matrix (dict)**: A dictionary representing the graph where the keys are tuples `(start_node, end_node)`, and the values are the travel times between these nodes.
- **nodes (dict)**: A dictionary where the keys are node IDs and the values are node attributes, including coordinates, inlinks, and outlinks.

### Return Values

- **time_from_start (float)**: The shortest time from the start to the end node.
- **Pathnodes (list)**: The sequence of nodes forming the shortest path.
- **Pathlinks (list)**: The list of path links, based on the `inlinks` and `outlinks` between nodes.

### Example of `nodes` Dictionary

Here’s an example of what the `nodes` dictionary looks like:

```python
nodes = {
    1: {
        "coordinates": [[0, 8]],  # Coordinates for node 1
        "inlinks": [[3], [5]],    # Nodes that link into node 1 (e.g., nodes 3 and 5)
        "outlinks": [[2], [4]]    # Nodes that node 1 links out to (e.g., nodes 2 and 4)
    },
    2: {
        "coordinates": [[10, 20]],  # Coordinates for node 2
        "inlinks": [[1]],           # Node 1 links into node 2
        "outlinks": [[3]]           # Node 2 links out to node 3
    },
    3: {
        "coordinates": [[15, 25]],  # Coordinates for node 3
        "inlinks": [[2]],           # Node 2 links into node 3
        "outlinks": [[4]]           # Node 3 links out to node 4
    }
}
```

### Example of Sparse Travel Time Matrix

Here is an example of what the `orig_sparse_travel_time_matrix` might look like:

```python
orig_sparse_travel_time_matrix = {
    ('1', '2'): 0.9813579320907593,  # Travel time between node 1 and node 2
}
```

### Running the Algorithm

Once the parameters are set up, run the Dijkstra function as follows:

```python
from dijkstra import dijkstra

time, path_nodes, path_links = dijkstra(start=1, end=4, list_nodes=[1, 2, 3, 4], orig_sparse_travel_time_matrix=orig_sparse_travel_time_matrix, nodes=nodes)
```

### Example Output

The function will return the shortest time, the path of nodes taken, and the path links, like this:

```python
Shortest Time: 5.0
Path: [1, 2, 4]
Path Links: [2, 4]
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
