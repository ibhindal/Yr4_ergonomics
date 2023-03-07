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
    
    Ex = point1[0]
    Ey = point1[1]
    Ez = point1[2]
    
    Fx = point2[0]
    Fy = point2[1]
    Fz = point2[2]
    
    # Calculate denominator - if this is 0, the line doesn't cross the plane
    td = A*Ex - A*Fx + B*Ey - B*Fy + C*Ez - C*Fz
    
    if td == 0:
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

def crossingPoint(plane, point1, point2):
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
    td = A*Ex - A*Fx + B*Ey - B*Fy + C*Ez - C*Fz        
    
    tn = D - A*Ex - B*Ey - C*Ez
    t = tn / td
    
    xcross = Ex + (Ex - Fx) * t
    ycross = Ey + (Ey - Fy) * t
    zcross = Ez + (Ez - Fz) * t
    
    crossingcoords = (np.array([xcross, ycross, zcross]))
    return crossingcoords
        
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

# Manually type coordinates into UI and store in the list below - UI to be completed later


start_1= np.array([33.271, -13.546, -73.915])  # replace with user input values
# edit as user input 

end_1 = np.array([-5.504,-13.546,-98.405])

print("Initial k-wire 1 point: ", start_1)
print("K-wire 1 end point", end_1)

# Using coordinates, calculate angle of trajectory from long axis of bone
# Long axis of bone is manually selected by technician/user - coordinates of start and end point are manually input, as above


axis_1 = np.array([11.286,-16.893,-70.172])

axis_2 = np.array([-6.286,-13.961,-128.351])

#Calculate angle of trajectory between the long axis of the bone and k-wire 1
# Calculate the slope of k_1

# Calculate the slope-intercept form for k1
m1 = (end_1[0] - start_1[0]) / (end_1[2] - start_1[2])
n1 = (end_1[1] - start_1[1]) / (end_1[2] - start_1[2])
p1 = 1

b1 = start_1[0] - m1 * start_1[2]
c1 = start_1[1] - n1 * start_1[2]
d1 = start_1[2]

#print(f"The slope-intercept form for line1 is [{m1:.2f}, {n1:.2f}, {b1:.2f}].")


# Calculate the slope of long axis of bone

# Calculate the slope-intercept form for long axis of bone

m2 = (axis_2[0] - axis_1[0]) / (axis_2[2] - axis_1[2])
n2 = (axis_2[1] - axis_1[1]) / (axis_2[2] - axis_1[2])
p2 = 1

b2 = axis_1[0] - m1 * axis_1[2]
c2 = axis_1[1] - n1 * axis_1[2]
d2 = axis_1[2]

#print(f"The slope-intercept form for line2 is [{m2:.2f}, {n2:.2f}, {b2:.2f}].")


# Calculate the angle between the two lines using the dot product and the arccosine function (np.arccos) and the magnitude (np.linalg.norm):

cos_theta = np.dot([m1, n1, -1], [m2, n2, -1]) / (np.linalg.norm([m1, n1, -1]) * np.linalg.norm([m2, n2, -1]))
theta = np.arccos(cos_theta)

print(f"The angle between the original line and the long axis of the bone is {np.degrees(theta):.2f} degrees.")

# Code undergoes verification

#Does it go through the fracture plane?

#Does it contact the articulating surface?
#Does the end point protrude away from the radius? (edge detection?)
#Does it cross other k-wires at the fracture level?

# If any of last 3 are yes:


#Centre of cuboid which is start_1 coordinates, are on the face of the cuboid (on saggital plane)

cuboid_points = []


# Define the length of the cuboid relative to the start point

cuboid_length_min = start_1[0] + 0
cuboid_length_max = start_1[0] + 6

# Define the width of the cuboid relative to the start point
cuboid_width_max= start_1[1] + 3
cuboid_width_min = start_1[1] - 3

# Define the height of the cuboid relative to the start point
cuboid_height_max = start_1[2] + 7
cuboid_height_min = start_1[2] - 7

# Use a nested for loop to store all the possible coordinates within the specified range menioned above
# arange() function creates a sequence of numbers that are evenly spaced within a specified range

for x in np.arange(cuboid_length_min, cuboid_length_max):
    for y in np.arange(cuboid_width_min, cuboid_width_max):
        for z in np.arange(cuboid_height_min, cuboid_height_max):
            cuboid_points.append([x, y, z])

#print(cuboid_points)

# Choose optimum start point that creates 45 degree angle from long axis of bone

# convert 45 degrees to radians
theta = np.radians(45)

# initialize variables for storing the best point and angle so far
best_point = None
best_angle_diff = np.inf

# iterate over all points in the cuboid_points list
for point in cuboid_points:
    # calculate the slope of line formed by current point and end_1
    
    m_new = (end_1[0] - point[0]) / (end_1[2] - point[2])
    n_new = (end_1[1] - point[1]) / (end_1[2] - point[2])

    
    # calculate the angle between the new line and the long axis of the bone
    cos_theta1 = np.dot([m_new, n_new, -1], [m2, n2, -1]) / (np.linalg.norm([m_new, n_new, -1]) * np.linalg.norm([m2, n2, -1]))
    theta1 = np.arccos(cos_theta1)

    cos_theta2 = np.dot([m_new, n_new, -1], [-m2, -n2, -1]) / (np.linalg.norm([m_new, n_new, -1]) * np.linalg.norm([-m2, -n2, -1]))
    theta2 = np.arccos(cos_theta2)
    
    # calculate the difference between the angle and 45 degrees
    angle_diff1 = abs(theta1 - theta)
    angle_diff2 = abs(theta2 - theta)
    
    # select the best point so far
    if angle_diff1 < best_angle_diff or angle_diff2 < best_angle_diff:
        best_point = point
        best_angle_diff = min(angle_diff1, angle_diff2)

print(f"The best k-wire 1 start point is {best_point} with angle difference of {np.degrees(best_angle_diff):.2f} degrees (from 45 degrees to long axis of bone).")






# =============================================================================
# Second k-wire 
# =============================================================================

# =============================================================================
# Second k-wire 
# =============================================================================

entry2nd = np.array([8.293667793273926,-3.8751466666720233,-78.97350782229576])

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

fullpointslist_2 = []

for i in listofentrypoints2nd:

    # Find the angle from the x axis
    alpha_2 = (180 / math.pi) * math.atan((long2[2] - long1[2]) / (long2[1] - long1[1]))
    angle_2 = 45 - alpha_2
    
    # Find equation of line
    mkwire_2 = math.tan(angle_2)
    ckwire_2 = i[2] - i[1] * mkwire_2
       
    # Create 2nd point on line
    Fx_2 = i[0]
    Fy_2 = i[1] + 100
    Fz_2 = mkwire_2 * Fy_2 + ckwire_2
    
    point2_2 = np.array([Fx_2, Fy_2, Fz_2])
    
    # Check line goes through plane
    crossesPlane_2 = checkCrossesPlane(fracture_plane, i, point2_2)
    
    if crossesPlane_2 == False:
        continue
    
  
    
    # Calculate end point
    edgeline1_2 = np.array([8.293667793273926,-20.673918930041154,-82.19624485596708])
    edgeline2_2 = np.array([8.293667793273926,-15.29739697044306,-105.40117338175465])
    
    medge_2 = (edgeline2_2[2] - edgeline1_2[2]) / (edgeline2_2[1] - edgeline1_2[1])
    cedge_2 = edgeline1_2[2] - medge_2 * edgeline1_2[1]
    
    yedge_2 = (cedge_2 - ckwire_2) / (mkwire_2 - medge_2)
    zedge_2 = mkwire_2 * yedge_2 + ckwire_2
    
    exitpoint = (i[0], yedge_2, zedge_2)
    
    # Save start point and end point
    fullpointslist_2.append([i, exitpoint])

    
# =============================================================================
# Third k-wire
# =============================================================================
"""
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
"""



# =============================================================================
# Checking Section
# - no intersections at fracture line
# - no intersections with nerves, arteries etc
# =============================================================================

    # Find crossing point on plane and save
    #crosspoint_2 = crossingPoint(fracture_plane, i, point2_2)  

# =============================================================================
# Preview image
# =============================================================================


# Section to convert to something Solidworks can use
