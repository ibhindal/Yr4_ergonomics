#a_star
import numpy as np
import random
from queue import PriorityQueue



# Define a function to find the shortest path between two points in a 3D model
def find_shortest_path(model, start_point, end_point, angle):
    # Extract the vertices and faces of the model
    vertices = model.vertices
    faces = model.faces

    # Create a binary image where white pixels represent allowed entry points and black pixels represent prohibited areas
    entry_map = np.zeros(vertices.shape, dtype=np.int8)

    # Set the starting and ending points in the entry map
    entry_map[start_point[0], start_point[1]] = 1
    entry_map[end_point[0], end_point[1]] = 2

    # Set the prohibited areas in the entry map
    prohibited_areas = np.argwhere(faces == 0)
    for prohibited_area in prohibited_areas:
        entry_map[prohibited_area[0], prohibited_area[1]] = -1

    # Find the coordinates of the entry points in the binary image
    entry_points = np.argwhere(entry_map == 1)

    # Use the random.choice() function to choose a random starting point for each line
    line1_start = random.choice(entry_points)
    line2_start = random.choice(entry_points)

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

