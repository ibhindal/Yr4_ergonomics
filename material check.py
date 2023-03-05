import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

# Load the STL file
your_file = mesh.Mesh.from_file('combined.stl')

# Extract material information if present
if hasattr(your_file, 'points'):
    materials = your_file.points[:, -1] # last column contains material information
else:
    materials = None

# Create a 3D plot
fig = plt.figure()
ax = mplot3d.Axes3D(fig)

# Plot the mesh, color each material differently if present
if materials is not None:
    unique_materials = np.unique(materials)
    for mat in unique_materials:
        indices = np.where(materials == mat)[0]
        ax.add_collection(mplot3d.art3d.Poly3DCollection(your_file.vectors[indices], alpha=0.2, facecolor=plt.cm.jet(mat/unique_materials.max())))
else:
    ax.add_collection(mplot3d.art3d.Poly3DCollection(your_file.vectors, alpha=0.2))

# Set the limits of the plot and show it
ax.auto_scale_xyz([-1, 1], [-1, 1], [-1, 1])
plt.show()
