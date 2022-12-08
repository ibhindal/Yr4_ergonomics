# Import the a_star and heuristic functions from the file where they are defined
from shortest_path import find_shortest_path
from a_star import a_star, heuristic
import numpy as np
import trimesh

# Load the STL model from a file
model = trimesh.load('model.stl')

# Define the starting and ending points of the lines
start_points = [(10, 10 , 10), (20, 10 ,20)]
end_points = [(100, 50 ,100), (200, 50,200)]

# Extract the vertices and faces of the model
vertices = model.vertices
faces = model.faces

# Create a binary image where white pixels represent allowed entry points and black pixels represent prohibited areas
entry_map = np.zeros(vertices.shape, dtype=np.int8)

# Loop through the start and end points
for start_point, end_point in zip(start_points, end_points):
    # Set the starting and ending points in the entry map
    entry_map[start_point[0], start_point[1]] = 1
    entry_map[end_point[0], end_point[1]] = 2

    # Set the prohibited areas in the entry map
    prohibited_areas = np.argwhere(faces == 0)
    for prohibited_area in prohibited_areas:
        entry_map[prohibited_area[0], prohibited_area[1]] = -1

    # Define a function to get the neighbors of a node
    # Define a function to get the neighbors of a node
    def get_neighbors(current_node):
    # Define the neighbors of the current node
        neighbors = [(current_node[0] + 1, current_node[1], current_node[2]), (current_node[0] - 1, current_node[1], current_node[2]), (current_node[0], current_node[1] + 1, current_node[2]), (current_node[0], current_node[1] - 1, current_node[2]), (current_node[0], current_node[1], current_node[2] + 1), (current_node[0], current_node[1], current_node[2] - 1)]

    # Filter out the neighbors that are outside the boundaries of the entry map
        neighbors = [neighbor for neighbor in neighbors if neighbor[0] >= 0 and neighbor[0] < entry_map.shape[0] and neighbor[1] >= 0 and neighbor[1] < entry_map.shape[1] and neighbor[2] >= 0 and neighbor[2] < entry_map.shape[2]]

        return neighbors


    # Call the a_star function to find the shortest path between the start and end points
    path = a_star(entry_map, start_point, end_point, heuristic, get_neighbors)

    # Print the path
    print(path)
