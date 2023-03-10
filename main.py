# =============================================================================
# Notes for this
# Input points:
#       - 2 points for long axis
#       - 2 points (entry and exit) per k-wire
#       - 3 points on fracture plane    
# Note: Solidworks Y and Z are opposite to Slicer Y and Z
# =============================================================================

import numpy as np
import math


# Setting up k-wire information
# Left or right hand will potentially make a difference in some of the code: left = 0, right = 1 - change this to box selection
handInput = input("Is this the left or right hand?")
if handInput.lower() == "left" or handInput.lower() == "l":
    handSide = 0
    print("Your arm is the left one")
    
elif handInput.lower() == "right" or handInput.lower() == "r":
    handSide = 1
    print("Your arm is the right one")


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
long1 = np.array([10.484512548250422,-14.307704321150922,-71.77198431949066])
long2 = np.array([-5.572349548339844,-14.094643592834473,-128.3506317138672]) ################# Error

if long1[0] == long2[0]:
    long1[0] += 0.000000003
    
elif long1[1] == long2[1]:
    long1[1] += 0.000000003
    
elif long1[2] == long2[2]:
    long1[2] += 0.000000003
    
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
    # 3D lines can be written as parametric equations in the form: x = u + at, y = v + bt, z = w + ct. 
    # If t is calculated for when the line crosses the plane, the x, y and z values can be calculated
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
    
    # Calculate denominator
    td = A*Ex - A*Fx + B*Ey - B*Fy + C*Ez - C*Fz        
    
    # Calculate numerator
    tn = D - A*Ex - B*Ey - C*Ez
    
    # Calculate t
    t = tn / td
    
    xcross = Ex + (Ex - Fx) * t
    ycross = Ey + (Ey - Fy) * t
    zcross = Ez + (Ez - Fz) * t
    
    crossingcoords = (np.array([xcross, ycross, zcross]))
    return crossingcoords

def lengthWire(point1, point2):
    # Find the distance between 2 points
    lsquared = (point2[0] - point1[0])**2 + (point2[1] - point1[1])**2 + (point2[2] - point1[2])**2
    l = lsquared ** 0.5
    
    return l

# =============================================================================
# Define the fracture plane
# =============================================================================

fracturecoord1 = np.array([14.077756881713867,-11.07859992980957,-92.56031036376953])                # User selects 3 points on the plane (points can't be colinear) - will change UI
fracturecoord2 = np.array([-0.03193238005042076,-10.694211959838867,-86.19048309326172])
fracturecoord3 = np.array([7.713603496551514,-19.633007049560547,-86.71790313720703])

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

entry1st = np.array([33.271, -13.546, -73.915])

cuboid_points = []

#The specified +/- ranges were taken from a cuboid ROI in Slicer
#Require some rough dimensions of this region from literature 

# Define the length of the cuboid relative to the start point
cuboid_length_min = entry1st[0] + 0
cuboid_length_max = entry1st[0] + 6

# Define the width of the cuboid relative to the start point
cuboid_width_max= entry1st[1] + 3
cuboid_width_min = entry1st[1] - 3

# Define the height of the cuboid relative to the start point
cuboid_height_max = entry1st[2] + 7
cuboid_height_min = entry1st[2] - 7

# Use a nested for loop to store all the possible coordinates within the specified range menioned above
# arange() function creates a sequence of numbers that are evenly spaced within a specified range

for x in np.arange(cuboid_length_min, cuboid_length_max):
    for y in np.arange(cuboid_width_min, cuboid_width_max):
        for z in np.arange(cuboid_height_min, cuboid_height_max):
            cuboid_points.append([x, y, z])


#Combined Isobel's code for exit point calculation
fullpointslist_1 = []

for i in cuboid_points:

    # Find the angle from the x axis
    alpha_1 = (180 / math.pi) * math.atan((long2[2] - long1[2]) / (long2[1] - long1[1]))
    angle_1 = 45 - alpha_1
    
    # Find equation of line
    mkwire_1 = math.tan(angle_1)
    ckwire_1 = i[2] - i[1] * mkwire_1
       
    # Create 2nd point on line
    Fx_2 = i[0]
    Fy_2 = i[1] + 100
    Fz_2 = mkwire_1 * Fy_2 + ckwire_1
    
    point2_1 = np.array([Fx_2, Fy_2, Fz_2])
    
    # Check line goes through plane
    crossesPlane_2 = checkCrossesPlane(fracture_plane, i, point2_1)
    
    if crossesPlane_2 == False:
        continue
    
    # Find crossing point on plane and save
    crosspoint = crossingPoint(fracture_plane, i, point2_1)    
    
    # Calculate end point
    edgeline1_2 = np.array([-4.15329933,-18.09798622,-85.37478638])
    edgeline2_2 = np.array([-11.87345505,-14.09032822,-126.0778656])
    
    medge_2 = (edgeline2_2[2] - edgeline1_2[2]) / (edgeline2_2[1] - edgeline1_2[1])
    cedge_2 = edgeline1_2[2] - medge_2 * edgeline1_2[1]
    
    yedge_2 = (cedge_2 - ckwire_1) / (mkwire_1 - medge_2)
    zedge_2 = mkwire_1 * yedge_2 + ckwire_1
    
    exitpoint = (i[0], yedge_2, zedge_2)
    
    # Save start point and end point --- Where is the start point in this? - Naomi :)
    fullpointslist_1.append([i, exitpoint])


#print("Exit points: ",kwire_1_exit)


# =============================================================================
# Second k-wire 
# =============================================================================

entry2nd = np.array([7.5939459800720215,-3.464972496032715,-80.25806427001953])

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

fullpointslist = []

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
    
    # Find crossing point on plane and save
    crosspoint = crossingPoint(fracture_plane, i, point2_2)    
    
    # Calculate end point
    edgeline1_2 = np.array([8.293667793273926,-20.673918930041154,-82.19624485596708])
    edgeline2_2 = np.array([8.293667793273926,-15.29739697044306,-105.40117338175465])
    
    medge_2 = (edgeline2_2[2] - edgeline1_2[2]) / (edgeline2_2[1] - edgeline1_2[1])
    cedge_2 = edgeline1_2[2] - medge_2 * edgeline1_2[1]
    
    yedge_2 = (cedge_2 - ckwire_2) / (mkwire_2 - medge_2)
    zedge_2 = mkwire_2 * yedge_2 + ckwire_2
    
    exitpoint = (i[0], yedge_2, zedge_2)
    
    # Save start point and end point
    fullpointslist.append([i, exitpoint])
    
# =============================================================================
# Third k-wire
# =============================================================================
entry3rd = np.array[-9.145, 3.769, -77.482];

# add list of points

radius = 5

circlecentre3rd = (entry3rd[0], entry3rd[2])

# Finding the max and min x and y values that could be within 5mm of selected entry
minXentry3rd = circlecentre3rd[0] - radius
maxXentry3rd = circlecentre3rd[0] + radius
minYentry3rd = circlecentre3rd[1] - radius
maxYentry3rd = circlecentre3rd[1] + radius

# Creating a list of potential entry points 
listofxentry3rd = np.arange(minXentry3rd, maxXentry3rd + 1, 1)         # Creating a selection of x values that are 1mm apart
listofyentry3rd = np.arange(minYentry3rd, maxYentry3rd + 1, 1)         # Creating a selection of y values that are 1mm apart

listofentrypoints3rd = []                              # Create a list of coordinates that are within 5mm of selected point
Z = entry3rd[1]

for X in listofxentry3rd:
    for Y in listofyentry3rd:
        if (X - circlecentre3rd[0]) ** 2 + (Y - circlecentre3rd[1]) ** 2 <= radius ** 2:      # Equation of a circle
            listofentrypoints3rd.append((X, Y, Z))                                 # Saving values that are in the circle

fullpointslist = []

for i in listofentrypoints3rd:

    # Find the angle from the x axis
    alpha_3 = (180 / math.pi) * math.atan((long2[2] - long1[2]) / (long2[1] - long1[1]))
    angle_3 = 45 - alpha_3
    
    # Find equation of line
    mkwire_3 = math.tan(angle_3)
    ckwire_3 = i[2] - i[1] * mkwire_3
       
    # Create 3rd point on line
    Fx_3 = i[0]
    Fy_3 = i[1] + 100
    Fz_3 = mkwire_3 * Fy_3 + ckwire_3
    
    point2_3 = np.array([Fx_3, Fy_3, Fz_3])
    
    # Check line goes through plane
    crossesPlane_3 = checkCrossesPlane(fracture_plane, i, point2_3)
    
    if crossesPlane_3 == False:
        continue
    
    # Find crossing point on plane and save
    crosspoint = crossingPoint(fracture_plane, i, point2_3)    
    
    # Calculate end point
    edgeline1_3 = np.array([8.293667793273926,-20.673918930041154,-82.19624485596708])
    edgeline2_3 = np.array([8.293667793273926,-15.29739697044306,-105.40117338175465])
    
    medge_3 = (edgeline2_3[2] - edgeline1_3[2]) / (edgeline2_3[1] - edgeline1_3[1])
    cedge_3 = edgeline1_3[2] - medge_3 * edgeline1_3[1]
    
    yedge_3 = (cedge_3 - ckwire_3) / (mkwire_3 - medge_3)
    zedge_3 = mkwire_3 * yedge_3 + ckwire_3
    
    exitpoint_3 = (i[0], yedge_3, zedge_3)
    
    # Save start point and end point
    fullpointslist.append([i, exitpoint_3])



# =============================================================================
# Checking Section
# - no intersections at fracture line
# - no intersections with nerves, arteries etc
# =============================================================================
valueswork = False

    


# =============================================================================
# Preview image
# - length of wire in bone
# =============================================================================


# Section to convert to something Solidworks can use - swap the Y and Z values around
