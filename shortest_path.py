#find shortest path

import cv2
import numpy as np
import trimesh
from queue import PriorityQueue
import random
import a_star

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

    # Use the A* algorithm to find the shortest path between the starting point and the ending point
    line1_path = a_star(entry_map, line1_start, end_point)
    line2_path = a_star(entry_map, line2_start, end_point)

    # Check if both lines have a path
    if not all([line1_path, line2_path]):
        # Use the random.choice() function to choose a different starting point for each line
        line1_start = random.choice(entry_points)
        line2_start = random.choice(entry_points)

        # Use the A* algorithm to find the shortest path between the starting point and the ending point
        line1_path = a_star(entry_map, line1_start, end_point)
        line2_path = a_star(entry_map, line2_start, end_point)

    # Return the paths for each line
    return line1_path, line2_path
