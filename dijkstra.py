import numpy as np
import itertools


def dijkstra(start, end, list_nodes, orig_sparse_travel_time_matrix, nodes):
    """
    Implements Dijkstra's algorithm to find the shortest path between two nodes in a graph.

    Parameters:
    start (int): The starting node.
    end (int): The target node (where the path ends).
    list_nodes (list): A list of all nodes in the graph.
    orig_sparse_travel_time_matrix (dict): A dictionary representing the graph where the keys are tuples (start_node, end_node)
                                           and the values are the travel times between these nodes.
    nodes (dict): Dictionary where keys are node indices and values contain attributes like 'coordinates', 'inlinks', and 'outlinks'.

    Returns:
    tuple: A tuple containing the shortest time from the start to the end node, the list of nodes forming the path,
           and a list of path links.

    Example of 'nodes' dictionary:

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
    Example of 'orig_sparse_travel_time_matrix' dictionary:
    orig_sparse_travel_time_matrix = { ('1', '2'): 0.9813579320907593} , where 1 and 2 are nodes and 0.9813579320907593 is the travel time between them in min

    """

    # Create a copy of the list of nodes and the travel time matrix to work with.
    unvisited_nodes = list_nodes.copy()
    sparse_travel_time_matrix = orig_sparse_travel_time_matrix.copy()

    # Initialize a dictionary to store the shortest time from the start node to each node, starting with infinity.
    time_from_start = {y: float("inf") for y in unvisited_nodes}
    time_from_start[start] = 0  # The time from the start node to itself is 0.

    round = 1  # Counter for the number of rounds of iteration.
    closed_nodes = []  # List to keep track of visited nodes.
    Pathnodes = {}  # Dictionary to store the path taken to reach each node.

    # Main loop: continue until the target node is reached.
    while True:
        if round == 1:
            # For the first round, start with the start node.
            close = start
            Pathnodes[close] = []  # Initialize the path for the start node.
            closed_nodes.append(close)  # Mark the start node as visited.
            unvisited_nodes.remove(close)  # Remove the start node from the unvisited list.

            # Initialize an empty NumPy array to hold the connected nodes and their travel times.
            list_connected_nodes = np.empty((0, 3), int)

            # Loop through the travel time matrix to find nodes connected to the start node.
            for key in sparse_travel_time_matrix.keys():
                if key[0] == str(close):
                    # Add each connection to the array.
                    dum_list = np.array((int(key[0]), int(key[1]), sparse_travel_time_matrix[key]))
                    list_connected_nodes = np.vstack((list_connected_nodes, dum_list))

            # Find the node with the minimum travel time from the start node.
            min_index = np.argmin(list_connected_nodes[:, 2])
            close = int(list_connected_nodes[min_index, 1])
            time_from_start[close] = list_connected_nodes[min_index, 2]  # Update the shortest time for this node.
            closed_nodes.append(close)  # Mark this node as visited.

            # Update the path taken to reach this node.
            if not Pathnodes[int(list_connected_nodes[min_index, 0])]:
                Pathnodes[close] = [int(list_connected_nodes[min_index, 0]), int(list_connected_nodes[min_index, 1])]
            else:
                Pathnodes[close] = [*Pathnodes[int(list_connected_nodes[min_index, 0])],
                                    int(list_connected_nodes[min_index, 1])]

            # Remove connections from the matrix that lead to the most recently visited node.
            keys_to_delete = [key for key in sparse_travel_time_matrix.keys() if close == int(key[1])]
            for key in keys_to_delete:
                del sparse_travel_time_matrix[key]

        else:
            # For subsequent rounds, continue with the most recently visited node.
            if closed_nodes[-1] in unvisited_nodes:
                unvisited_nodes.remove(closed_nodes[-1])

            # Reinitialize the list of connected nodes for the current round.
            list_connected_nodes = np.empty((0, 3), int)
            for i in range(len(closed_nodes)):
                for key in sparse_travel_time_matrix.keys():
                    if key[0] == str(closed_nodes[i]):
                        # Calculate the new travel time to the connected nodes.
                        dum_list = np.array(
                            (int(key[0]), int(key[1]), (sparse_travel_time_matrix[key] + time_from_start[int(key[0])])))
                        list_connected_nodes = np.vstack((list_connected_nodes, dum_list))

            # Find the node with the minimum travel time from the set of unvisited nodes.
            min_index = np.argmin(list_connected_nodes[:, 2])
            close = int(list_connected_nodes[min_index, 1])
            time_from_start[close] = list_connected_nodes[min_index, 2]
            if close not in closed_nodes:
                closed_nodes.append(close)

            # Update the path taken to reach this node.
            if not Pathnodes[int(list_connected_nodes[min_index, 0])]:
                Pathnodes[close] = [int(list_connected_nodes[min_index, 0]), int(list_connected_nodes[min_index, 1])]
            else:
                Pathnodes[close] = [*Pathnodes[int(list_connected_nodes[min_index, 0])],
                                    int(list_connected_nodes[min_index, 1])]

            # Remove the connections leading to the most recently visited node from the matrix.
            keys_to_delete = [key for key in sparse_travel_time_matrix.keys() if close == int(key[1])]
            for key in keys_to_delete:
                del sparse_travel_time_matrix[key]

        # Exit the loop if the target node has been reached.
        if end in closed_nodes:
            break
        round += 1

    # Construct the list of path links from the Pathnodes dictionary.
    Pathlinks = []
    i = 1
    while i < len(Pathnodes[end]):
        Pathlinks.append(int(*list(set(itertools.chain(*nodes[Pathnodes[end][i - 1]].outlinks)).intersection(
            set(itertools.chain(*nodes[Pathnodes[end][i]].inlinks))))))
        i += 1

    # Return the shortest time to the target node, the path taken to reach it, and the path links.
    return time_from_start[end], Pathnodes[end], Pathlinks
