import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
#pip install numpy-stl - this allows the below import to be performed
from stl import mesh
import os

current_directory =os.getcwd()
print(current_directory)

"""
#Checking format of STL file
with open('Lizzy/Radius1.stl', 'r', encoding='utf-8', errors='ignore') as file:
    first_line = file.readline()
    if first_line.startswith('solid'):
        print('ASCII format')
    else:
        print('Binary format')
"""

#Function that draws line. This will depend on the coordinates of the point selected

#This code defines the start and end points of the line
def draw_line(ax1, start, end):
    
    x = [start[0], end[0]]
    y = [start[1], end[1]]
    z = [start[2], end[2]]

    ax1.plot3D(x,y,z, 'red')

def main():

    #Load the 3D STL file
    #os.chdir('C:\Users\naomi\OneDrive\Documents\Year_4\Ergonomics\Slicer\Segmentation')
    Radius_3D = mesh.Mesh.from_file('Lizzy/Cube.stl')



    #Define the start and end points

    start = np.array([0,0,0])
    end = np.array([10,10,10])

    #Calculate angle of trajectory

    delta = end - start
    angle = np.arctan2(delta[1], delta[0])

    #Create a figure and axes

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    #Draw the 3D STL file
    #...

    #Draw the line

    draw_line(ax, start,end)

    plt.show()

if __name__ == '__main__':
    main()


#Attempt to fix stl not being shown in figure
"""
    vertices = Radius_3D.points
    faces = Radius_3D.vectors
    normals = Radius_3D.normals
    
    vertices = np.array(vertices, dtype=int)
    faces = np.array(faces, dtype=int)  


    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, projection='3d')
    ax1.add_collection(Poly3DCollection(vertices[faces], facecolor='cyan', alpha=.25))

    ax1.set_xlim([0, Radius_3D.points[:, 0].max()])
    ax1.set_ylim([0, Radius_3D.points[:, 1].max()])
    ax1.set_zlim([0, Radius_3D.points[:, 2].max()])
                 
    plt.show()

    """