#a_star
import numpy as np
import random
from queue import PriorityQueue

# Define a function to get the neighbors of a node
# Define a function to get the neighbors of a node
def get_neighbors(current_node):
    # Define the neighbors of the current node
    neighbors = [(current_node[0] + 1, current_node[1], current_node[2]), (current_node[0] - 1, current_node[1], current_node[2]), (current_node[0], current_node[1] + 1, current_node[2]), (current_node[0], current_node[1] - 1, current_node[2]), (current_node[0], current_node[1], current_node[2] + 1), (current_node[0], current_node[1], current_node[2] - 1)]

    # Filter out the neighbors that are outside the boundaries of the entry map
    neighbors = [neighbor for neighbor in neighbors if neighbor[0] >= 0 and neighbor[0] < entry_map.shape[0] and neighbor[1] >= 0 and neighbor[1] < entry_map.shape[1] and neighbor[2] >= 0 and neighbor[2] < entry_map.shape[2]]

    return neighbors


# Define a function to calculate the heuristic cost of moving from one point to another
def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

# Use the A* algorithm to find the shortest path between the starting point and the ending point
def a_star(entry_map, start, end):
    # Create a priority queue to store the nodes to be explored
    queue = PriorityQueue()

    # Add the starting node to the priority queue
    queue.put((0, start))

    # Create a dictionary to store the distances from the starting node to all other nodes
    distances = {}
    distances[start] = 0

    # Create a dictionary to store the paths between the starting node and all other nodes
    paths = {}
    paths[start] = [start]

    # Create a set to store the visited nodes
    visited = set()
    # Define the neighbors of the current node
    neighbors = [(current_node[0] + 1, current_node[1]),
                (current_node[0] - 1, current_node[1]),
                (current_node[0], current_node[1] + 1),
                (current_node[0], current_node[1] - 1)]

    # Loop until the priority queue is empty
    while not queue.empty():
        # Get the next node from the priority queue
        current_distance, current_node = queue.get()

        # Check if the current node has been visited
        if current_node in visited:
            continue

        # Add the current node to the visited set
        visited.add(current_node)

        # Check if the current node is the ending node
        if current_node == end:
            # Return the path from the starting node to the ending node
            return paths[current_node]

        # Loop through the neighbors of the current node
        
        for neighbor in neighbors:
            # Check if the neighbor is a prohibited area
            if entry_map[neighbor] == -1:
                continue

            # Calculate the distance from the starting node to the neighbor
            distance = current_distance + heuristic(current_node, neighbor)

            # Check if the neighbor is already in the distances dictionary
            if neighbor in distances:
                # Update the distance in the distances dictionary if the new distance is shorter
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    paths[neighbor] = paths[current_node] + [neighbor]
                    queue.put((distance, neighbor))
            else:
                # Add the neighbor to the distances dictionary if it is not already in the dictionary
                distances[neighbor] = distance
                paths[neighbor] = paths[current_node] + [neighbor]
                queue.put((distance, neighbor))

