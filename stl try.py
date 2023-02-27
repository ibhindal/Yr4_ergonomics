from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

class LineDrawer:
    def __init__(self, axes, mesh):
        self.axes = axes
        self.mesh = mesh
        self.start_point = None
        self.end_point = None
        self.line = None
        self.cid = axes.figure.canvas.mpl_connect('button_press_event', self.on_press)

    def on_press(self, event):
        if event.button == 1: # left mouse button
            if self.start_point is None:
                self.start_point = (event.xdata, event.ydata)
                self.end_point = None
                self.line = None
            else:
                if self.start_point is not None:
                    self.end_point = (event.xdata, event.ydata)
                    if self.line is not None:
                        self.line.remove()
                    self.line, = self.axes.plot([self.start_point[0], self.end_point[0]], [self.start_point[1], self.end_point[1]], color='red')
                    self.start_point = None
                    self.end_point = None

                    # Modify the STL
                    vertex = self.mesh.vectors[0][0]
                    vector = [self.end_point[0] - self.start_point[0], self.end_point[1] - self.start_point[1], 0.0]
                    vertex += vector
                    self.mesh.update_normals()

                    # Redraw the mesh
                    self.axes.collections.clear()
                    self.axes.add_collection3d(mplot3d.art3d.Poly3DCollection(self.mesh.vectors))

    def disconnect(self):
        self.axes.figure.canvas.mpl_disconnect(self.cid)


#Using an existing stl file:
your_mesh = mesh.Mesh.from_file('whole.stl')

# Create a new plot
figure = pyplot.figure()
axes = figure.add_subplot(projection='3d')

# Load the STL files and add the vectors to the plot
your_mesh = mesh.Mesh.from_file('whole.stl')
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

# Auto scale to the mesh size
scale = your_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)

# Add line drawing and STL modification functionality
line_drawer = LineDrawer(axes, your_mesh)

# Show the plot to the screen
pyplot.show()
