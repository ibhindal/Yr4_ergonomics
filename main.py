# =============================================================================
# Notes for this
# Input points:
#       - 2 points for long axis
#       - 2 points (entry and exit) per k-wire
#       - 3 points on fracture plane    
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import math
import cv2


# Setting up k-wire information
# Left or right hand will potentially make a difference in some of the code: left = 0, right = 1 - change this to box selection
handInput = input("Is this the left or right hand?")
if handInput.lower() == "left" or handInput.lower() == "l":
    handSide = 0
    print("Your arm is the left one")
    
elif handInput.lower() == "right" or handInput.lower() == "r":
    handSide = 1
    print("Your arm is the right one")

angleofentry = 45               # This is taken from research as the ideal angle


# User can input a k-wire thickness or type x which chooses the average value for them - change this to box selection
kWireDiameterInput = input("Enter the diameter of your k-wire in mm. If none is decided, type x: ")
 
 
try:
     kWireDiameter = float(kWireDiameterInput) # Convert to float
 
     if kWireDiameter < 0.5:
         print("This value is too small")
 
     elif kWireDiameter > 3:
         print("This value is too big")

except(ValueError):
     if kWireDiameterInput.lower() == "x": # Code to choose value for user 
         kWireDiameter = 1.8 # Research needed on what diameter is best/most commonly used
 
except:
     print("This is not a valid number")
 

print("Your k-wire diameter is " + str(kWireDiameter))

# Select two points for the long axis
long1 = np.array([10.671098037037027,-16.05396500000001,-71.40649860082304])
long2 = np.array([-6.576912251028801,-16.05396500000001,-128.03204181069958])

# =============================================================================
# Functions - may be needed multiple times so include here
# =============================================================================
def checkCrossesPlane(plane, point1, point2):
    A = plane[0]
    B = plane[1]
    C = plane[2]
    D = plane[3]
    
    Ex = point1[0]
    Ey = point1[1]
    Ez = point1[2]
    
    Fx = point2[0]
    Fy = point2[1]
    Fz = point2[2]
    
    # Calculate denominator - if this is 0, the line doesn't cross the plane
    t = A*Ex - A*Fx + B*Ey - B*Fy + C*Ez - C*Fz
    
    if t == 0:
        return False
    else:
        return True
    
def checkAngle(points, long1, long2):
    # Find gradient of the propose k wire
    point1 = points[0]
    point2 = points[1]
    
    point1 = points[0]
    point2 = points[1]
    
    Ax = point2[0] - point1[0]
    Ay = point2[1] - point1[1]
    Az = point2[2] - point1[2]
    
    Bx = long2[0] - long1[0]
    By = long2[1] - long1[1]
    Bz = long2[2] - long1[2]
    
    test = (Ax*Bx + Ay*By + Az*Bz)
    test2 = ((Ax**2 + Ay**2 + Az**2)**0.5) * ((Bx**2 + By**2 + Bz**2)**0.5)
    angle = math.acos(test / test2) * (180 / math.pi)
    
    return angle

# =============================================================================
# Define the fracture plane
# =============================================================================

fracturecoord1 = np.array([-2.3462682181069994,-16.05396500000001,-87.02733810699588])                # User selects 3 points on the plane (points can't be colinear) - will change UI
fracturecoord2 = np.array([13.358031272888184,-12.44699478149414,-96.24616241455078])
fracturecoord3 = np.array([4.430776596069336,-7.407128810882568,-90.65580749511719])

# Calculate normal vector of fracture plane
vector1 = fracturecoord2 - fracturecoord1
vector2 = fracturecoord3 - fracturecoord1
normal = np.cross(vector1, vector2)
a=normal[0]
b=normal[1]
c=normal[2]

# create a new vector from the normal and any of the original points
 # and use it to find the d coefficient of the plane
d = np.dot(normal, fracturecoord1)

fracture_plane = [a, b, c, d]  # plane equation: a*x + b*y + c*z = d
#for the above  a, b and c are the simplified normal vector and d is if you sub in any of the fracture coordinates
#into the plane equation and equate to zero


#THIS NEEDS LIMITS TO HOW BIG TO MAKE IT.      


# =============================================================================
# First k-wire
# =============================================================================



coordinatesRadialStyloid = np.array([R,A,S]) # To be transformed
 
# Define start and end points
getNode('R') # should return values Rmin, Rmax, Amin, Amax, Smin and Smax

start_point= [25.838743209838868, -11.009124755859375, -71.25559997558594]
K1_volume = [2.97403722171164, 7.436612744439172, 9.758928644823208]
point_on_plane=[10 ,20,50] # this is a random point now. it should be a point on the fracture plane and will eventuslly be changed to all the ponts in the fracture plane.
end = np.array([4, 5, 6]) # change this to use isobels function instead
 

x1_1 = start_point[0]  # getting the value of start point coord. and initilaizing variables. the _1 refers to first k wire so that others an use xyand z without consequence
y1_1 = start_point[1]
z1_1 = start_point[2]
 
x2_1 = point_on_plane[0]  # getting the value of point on fracture plane coord. and initilaizing variables
y2_1 = point_on_plane[1]
z2_1 = point_on_plane[2]

x3_1= end[0]#same for end. will change to isobel code later when modified to 3D
y3_1= end[1]
z3_1= end[2]

#Making a cube to get a range of start points
# Define the start point as the center of one face of the cube and the side length r
#need to agree on this
r = 10  #sidelength
 
# Generate a list of all points within the cube
startpoints1 = []
for theta in range(0, 360):
    for phi in range(0, 180):
        x = x1_1 + r * (np.cos(theta) * np.sin(phi)+1)/2
        y = y1_1 + r * (np.sin(theta) * np.sin(phi)+1)/2
        z = z1_1 + r * (np.cos(phi)+1)/2
        startpoints1.append([x, y, z])
 
best_lines = []
for point in startpoints1:
    start_point = point
 
    # Calculate the distance from the start point to the point on the plane
    distance_to_plane = ((x1_1 - x2_1)**2 + (y1_1 - y2_1)**2 + (z1_1 - z2_1)**2)**0.5
 
    # Calculate the distance from the point on the plane to the detected edge point
    distance_to_edge = ((x2_1 - x3_1)**2 + (y2_1 - y3_1)**2 + (z2_1 - z3_1)**2)**0.5
 
    # Choose the line that has the shortest length
    if distance_to_plane + distance_to_edge < distance_to_plane:
        best_line = [start_point, detected_edge_point]
    else:
        best_line = [start_point, point_on_plane, detected_edge_point]
 
    # Find the angle between the line connecting the start point to the point on the plane and the line connecting the point on the plane to the detected edge point
    cos_angle = ((x1_1 - x2_1)*(x2_1 - x3_1) + (y1_1 - y2_1)*(y2_1 - y3_1) + (z1_1 - z2_1)*(z2_1 - z3_1)) / (distance_to_plane * distance_to_edge)

    # Choose the line that is as close to 45 degrees to the long axis as possible and has the shortest length
    if cos_angle < 0.70710678118:  # 45 degrees = pi/4 = 0.70710678118
        best_line = [start_point, point_on_plane]
    else:
        best_line = [point_on_plane, detected_edge_point]
 





# =============================================================================
# Second k-wire 
# =============================================================================

entry2nd = np.array([8.293667793273926,-3.8751466666720233,-78.97350782229576])
exit2nd = np.array([8.293667793273926,-19.152924444449795,-91.42206749307765])

radius = 5          # 5 mm ulnar to Lister's tubercle - used as a radius
circlecentre2nd = (entry2nd[0], entry2nd[2])

# Finding the max and min x and y values that could be within the tubercle
minXentry2nd = circlecentre2nd[0] - radius
maxXentry2nd = circlecentre2nd[0] + radius
minYentry2nd = circlecentre2nd[1] - radius
maxYentry2nd = circlecentre2nd[1] + radius

# Creating a list of potential entry points 
listofxentry2nd = np.arange(minXentry2nd, maxXentry2nd + 1, 1)         # Creating a selection of x values that are 1mm apart
listofyentry2nd = np.arange(minYentry2nd, maxYentry2nd + 1, 1)         # Creating a selection of y values that are 1mm apart

listofentrypoints2nd = []                              # Create a list of coordinates that are within our Lister's tubercle circle
Z = entry2nd[1]

for X in listofxentry2nd:
    for Y in listofyentry2nd:
        if (X - circlecentre2nd[0]) ** 2 + (Y - circlecentre2nd[1]) ** 2 <= radius ** 2:      # Equation of a circle
            listofentrypoints2nd.append((X, Y, Z))                                 # Saving values that are in the circle





# Creating a list of potential exit points 
# Modeling the potential exit points as on a straight line
distance2nd = 5         # How far away from the chosen entry point

minZexit2nd = exit2nd[2] - distance2nd
maxZexit2nd = exit2nd[2] + distance2nd

listofZexit2nd = np.arange(minZexit2nd, maxZexit2nd + 1, 1)         # Creating a selection of x values that are 1mm apart
Xexit2nd = exit2nd[0]
Yexit2nd = exit2nd[1]

listofexitpoints2nd = [(Xexit2nd, Yexit2nd, Z) for Z in listofZexit2nd]         
combinedentryexit2nd = [[a, b] for a in listofentrypoints2nd for b in listofexitpoints2nd]

# Checking if it crosses the fracture plane - returns a list of potential start and end points
finallist2nd = []

for i in combinedentryexit2nd:
    result = checkCrossesPlane(fracture_plane, i[0], i[1])
    
    if result == True:
        finallist2nd.append(i)

checkangles2nd = []

for i in finallist2nd:
    angle = checkAngle(i, long1, long2)
    
    if angle > 40 and angle <= 45:          ###### Need values!!!!
        checkangles2nd.append(i)

# =============================================================================
# Third k-wire
# =============================================================================
start_point3= [-9.145, 3.769, -77.482]
end_point3= [5.904, 18.973, -120.381]

# Determine coordinates x,y,z of start point
x1_3 = start_point3[0]
y1_3 = start_point3[1]
z1_3 = start_point3[2]

# Determine coordinates x,y,z of end point
x2_3 = end_point3[0]
y2_3 = end_point3[1]
z2_3 = end_point3[2]

# Initialize list of points
start_points3 = []
end_points3 = []

# Generate random points within a sphere centered at the start point chosen by user
for i in range(num_points):
    # Generate random coordinates within a sphere of radius L value (to be determined)
    r = L * math.sqrt(random.uniform(0, 1))
    theta = random.uniform(0, 2 * math.pi)
    phi = math.acos(1 - 2 * random.uniform(0, 1))
    x1_randS3 = x1_3 + r * math.sin(phi) * math.cos(theta)
    y1_randS3 = y1_3 + r * math.sin(phi) * math.sin(theta)
    z1_randS3 = z1_3 + r * math.cos(phi)
    x2_randE3 = x2_3 + r * math.sin(phi) * math.cos(theta)
    y2_randE3 = y2_3 + r * math.sin(phi) * math.sin(theta)
    z2_randE3 = z2_3 + r * math.cos(phi)
    

    # Add the random point to the list
    start_points3.append((x1_randS3, y1_randS3, z1_randS3))
    end_points3.append((x2_randE3, y2_randE3, z2_randE3))

return start_points3
return end_points3
#how to choose points?


# Determine Vector of K-wire 3 between start and end point 
vectorK3 = (x2_3 - x1_3, y2_3 - y1_3, z2_3 - z1_3)

# Calculate the parameter t of the line equation for the intersection point with the fracture plane
    t_3 = -(a*start_point3[0] + b*start_point3[1] + c*start_point3[2] + d) / (a*vectorK3[0] + b*vectorK3[1] + c*vectorK3[2]) # uses a,b,c,d from fracture_plane

# Calculate the intersection point
    intersection_3 = [start_point3[0] + t*vectorK3[0], start_point3[1] + t*vectorK3[1], start_point3[2] + t*vectorK3[2]]

# Check if the intersection point lies on the line segment
if (intersection_3[0] - start_point3[0])/vectorK3[0] == (intersection_3[1] - start_point3[1])/vectorK3[1] == (intersection_3[2] - start_point3[2])/vectorK3[2]:
    return True
else:
    return False




# =============================================================================
# Checking Section
# - no intersections at fracture line
# - no intersections with nerves, arteries etc
# =============================================================================


# =============================================================================
# Preview image
# =============================================================================


# Section to convert to something Solidworks can use
