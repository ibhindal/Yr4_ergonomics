import cv2
import numpy as np
import trimesh
from queue import PriorityQueue
import shortest_path
import a_star

# Load the STL model from a file
model = trimesh.load('model.stl')

# Define the starting and ending points of the line. random numbers dor now but this would start at green and end at break
start_point = (10, 10)
end_point = (100, 100)

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


