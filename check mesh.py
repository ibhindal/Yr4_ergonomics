import numpy as np
from sfepy.discrete.fem import Mesh

# Load the mesh from file
mesh = Mesh.from_file('combined.vtk')

# Get the cell connectivity array
conn = mesh.get_conn('2_3')

# Get the unique values of the number of vertices in each cell
cell_dims = np.unique(conn.shape[1])

# Print the dimensions of cells in the mesh
print('Cell dimensions:', cell_dims)
