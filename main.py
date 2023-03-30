# =============================================================================
# Notes for this
# Input points:
#       - 1 line for long axis
#       - 1 point (entry) per k-wire
#       - 3 points on fracture plane   
#       - 3 lines for each end of wire  
# Note: Solidworks Y and Z are opposite to Slicer Y and Z
# =============================================================================

import numpy as np
import math
import csv
import os

from tkinter import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory


root = Tk()
root.title('Ergonomics Distal Radial Fracture') # Set title of window (can be changed)
root.geometry("200x200") # Set size of window

filename = askopenfilename()

with open(filename, 'r') as file:
    csvreader = csv.reader(file)
    for index, row in enumerate (csvreader):

        if index == 1:
            E1_R = row[1] # R for K-wire 1
        if index == 1:
            E1_A = row[2] # A for K-wire 1
        if index == 1:
            E1_S = row[3] # S for K-wire 1
        if index == 2:
            E2_R = row[1] # R for K-wire 2
        if index == 2:
            E2_A = row[2] # A for K-wire 2
        if index == 2:
            E2_S = row[3] # S for K-wire 2
        if index == 3:
            E3_R = row[1] # R for K-wire 3
        if index == 3:
            E3_A = row[2] # A for K-wire 3
        if index == 3:
            E3_S = row[3] # S for K-wire 3
        if index == 4:
            L1_R = row[1] # R for long start
        if index == 4:
            L1_A = row[2] # A for long start
        if index == 4:
            L1_S = row[3] # S for long start
        if index == 5:
            L2_R = row[1] # R for long end
        if index == 5:
            L2_A = row[2] # A for long end
        if index == 5:
            L2_S = row[3] # S for long end
        if index == 6:
            F1_R = row[1] # R for point 1 fracture plane
        if index == 6:
            F1_A = row[2] # A for point 1 fracture plane
        if index == 6:
            F1_S = row[3] # S for point 1 fracture plane
        if index == 7:
            F2_R = row[1] # R for point 2 fracture plane
        if index == 7:
            F2_A = row[2] # A for point 2 fracture plane
        if index == 7:
            F2_S = row[3] # S for point 2 fracture plane
        if index == 8:
            F3_R = row[1] # R for point 3 fracture plane
        if index == 8:
            F3_A = row[2] # A for point 3 fracture plane
        if index == 8:
            F3_S = row[3] # S for point 3 fracture plane

def show():
    myLabel = clicked.get()
    myLabel2 = clicked2.get()
    myLabel3 = clicked3.get()
    root.quit()
    
options = ["2", "3"] # Set options for number of K-Wires
options2 = ["0.7", "0.8", "0.9", "1.0", "1.1", "1.2", "1.25", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", "1.9", "2.0", "2.2", "2.5", "2.8", "3.0"] # Set options of different diameters
options3 = ["left", "right"] # Set options for side of Hand

clicked = StringVar()
clicked.set(options[0])

clicked2 = StringVar()
clicked2.set(options2[0])

clicked3 = StringVar()
clicked3.set(options3[0]) 

drop = OptionMenu(root, clicked, *options)
drop.grid(row=1, column=0)

drop2 = OptionMenu(root,clicked2, *options2)
drop2.grid(row=3, column=0)
	    
drop3 = OptionMenu(root,clicked3, *options3)
drop3.grid(row=5, column=0)
	    
optionsLabel = Label(root, text="How many wires do you wish to use?").grid(row=0, column=0)
options2Label = Label(root, text="What diameter is the k-wire in mm").grid(row=2, column=0)
options3Label = Label(root, text="Is this the left or right Hand?").grid(row=4, column=0)
myButton = Button(root, text="Confirm Selection", command=show).grid(row=6, column=0)
root.mainloop()


numberWires = int(clicked.get())
kWireDiameter = float(clicked2.get())
handInput = clicked3.get()

# Left or right hand will potentially make a difference in some of the code: left = 0, right = 1
if handInput.lower() == "left" or handInput.lower() == "l":
    handSide = 0
    print("Your arm is the left one")
    
elif handInput.lower() == "right" or handInput.lower() == "r":
    handSide = 1
    print("Your arm is the right one")
 

print("Your k-wire diameter is " + str(kWireDiameter) + "\n")
###########################################################################################

# Select two points for the long axis
long1 = np.array([L1_R,L1_A,L1_S]).astype(float)
long2 = np.array([L2_R,L2_A,L2_S]).astype(float)

if long1[0] == long2[0]:
    long1[0] += 0.000000003
    
elif long1[1] == long2[1]:
    long1[1] += 0.000000003
    
elif long1[2] == long2[2]:
    long1[2] += 0.000000003

angle = math.radians(45) # Angle of long axis to wire
tanangle = round(math.tan(angle))
    
# =============================================================================
# Functions - may be needed multiple times so include here
# =============================================================================
def checkCrossesPlane(plane, point1, point2):
    # This code checks that the wire line created crosses the fracture plane
    # Defining variables
    A = plane[0]
    B = plane[1]
    C = plane[2]
    
    Ex = point1[0]
    Ey = point1[1]
    Ez = point1[2]
    
    Fx = point2[0]
    Fy = point2[1]
    Fz = point2[2]
    
    # Calculate denominator - if this is 0, the line doesn't cross the plane so is not a working trajectory
    td = A*Ex - A*Fx + B*Ey - B*Fy + C*Ez - C*Fz
    
    if td == 0:
        return False
    
    else:
        return True

def crossingPoint(plane, point1, point2):
    # Calculates the point on the plane that the line intersects it
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

def sortList(entry, points):
    # Sort list of values based on how close they are to the landmarks
    calculatedistance = []
    
    # Calculate the distance between landmark and wire entry
    for i in points:
        distance = math.sqrt((i[0] - entry[0])**2 + (i[1] - entry[1])**2 + (i[2] - entry[2])**2)
        calculatedistance.append([i[0], i[1], i[2], distance])
    
    # Sort list of calcualted distances
    calculatedistance.sort(key = lambda x: x[3])
    listdistances = [(i[0], i[1], i[2]) for i in calculatedistance]

    return listdistances

def checkIntersect(line1, line2):
    # Finding the intersection point of 2 lines using simultaneous equations. 
    # Uses the points [a, b, c] [d, e, f] for line 1 and [g, h, i] [j, k, l] for line 2
    # These points are converted to straight line equations in the form r = [point] * [difference in points]y and r = [point] * [difference in points]u
    # Defining the individual components
    a = line1[0][0]
    b = line1[0][1]
    c = line1[0][2]
    d = line1[1][0]
    e = line1[1][1]
    f = line1[1][2]
    
    g = line2[0][0]
    h = line2[0][1]
    i = line2[0][2]
    j = line2[1][0]
    k = line2[1][1]
    l = line2[1][2]
    
    # Calculates u value - if the denominator is 0, the lines dont cross
    denom = (b - e) * (g - j) - (a - d) * (h - k)
    if denom == 0:
        return True
    
    u = ((a - d) * (h - b) - (b - e) * (g - a)) / denom
    
    # Calculates y value
    denom2 = b - e
    if denom2 == 0:
        return True
    
    y = (h - b + (h - k) * u) / denom
    
    # Checks if these satisfy the 3rd equation - if they do, the lines intersect
    LHS = c + (c - f) * y
    RHS = i + (i - l) * u

    if LHS == RHS:
        return False
 
    return True
    
def distancePoints(point1, point2):
    # Find the distance between 2 points - pythagoras
    lsquared = (point2[0] - point1[0])**2 + (point2[1] - point1[1])**2 + (point2[2] - point1[2])**2
    l = lsquared ** 0.5
    
    return l

def swapYZ(currentY, currentZ):
    newZ = currentY
    newY = currentZ
    
    return newY, newZ

# =============================================================================
# Define the fracture plane
# =============================================================================
# User selects 3 points on the plane (points can't be colinear) - will change UI
fracturecoord1 = np.array([F1_R,F1_A,F1_S]).astype(float)              
fracturecoord2 = np.array([F2_R,F2_A,F2_S]).astype(float)
fracturecoord3 = np.array([F3_R,F3_A,F3_S]).astype(float)

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
# Coordinates of radial styloid
entry1st = np.array([E1_R,E1_A,E1_S]).astype(float)

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
            cuboid_points.append((x, y, z))

# Used to sort entry points by closest to initial chosen value
cuboid_points_sorted_1 = sortList(entry1st, cuboid_points)

# Exit point calculation
fullpointslist_1 = []
edgeline1_1 = np.array([1.2287021896347312,-10.309171676635742,-76.41708727152934])
edgeline2_1 = np.array([-0.8351931987676409,-10.309171676635742,-100.88898973401454])

for i in cuboid_points_sorted_1:
    # Find equation of line that is n degrees to the long axis
    mLA_1 = (long1[2] - long2[2]) / (long1[0] - long2[0])
    cLA_1 = long1[2] - (mLA_1 * long1[0])
    
    # Using tan a = (m1 - m2)/(1 + m1m2) to get gradient of k wire
    m_1 = (mLA_1 - 1) / (mLA_1 + 1)
    c_1 = i[2] - (m_1 * i[0])
    
    # Calculate equation of the edge of the bone
    medge_1 = (edgeline1_1[2] - edgeline2_1[2]) / (edgeline1_1[0] - edgeline2_1[0])
    cedge_1 = edgeline1_1[2] - (medge_1 * edgeline1_1[0])
    
    # Calculate the intersection of the edge of the bone and the wire to find end point
    xexit_1 = (c_1 - cedge_1) / (medge_1 - m_1)
    zexit_1 = (medge_1 * xexit_1) + cedge_1
    
    exitpoint_1 = (xexit_1, i[1], zexit_1)    
    
    # Check that the line calculated crosses the fracture plane
    crossesPlane_1 = checkCrossesPlane(fracture_plane, i, exitpoint_1)
    
    if crossesPlane_1 == False:
        continue

    
    # Save start point and end point
    fullpointslist_1.append([i, exitpoint_1])


#print("Exit points: ",kwire_1_exit)


# =============================================================================
# Second k-wire 
# =============================================================================
# Coordinates of the Lister's tubercle
entry2nd = np.array([E2_R,E2_A,E2_S]).astype(float)

radius = 5          # 5 mm ulnar to Lister's tubercle - used as a radius
circlecentre2nd = (entry2nd[0], entry2nd[2])

# Finding the max and min x and y values that could be within the tubercle
minXentry2nd = circlecentre2nd[0] - radius
maxXentry2nd = circlecentre2nd[0] + radius
minYentry2nd = circlecentre2nd[1] - radius
maxYentry2nd = circlecentre2nd[1] + radius

# Creating a list of potential entry points 
listofxentry2nd = np.arange(minXentry2nd, maxXentry2nd + 1, 1)         
listofyentry2nd = np.arange(minYentry2nd, maxYentry2nd + 1, 1)         

# Create a list of coordinates that are within the Lister's tubercle circle
listofentrypoints2nd = []                              
Z = entry2nd[1]

for X in listofxentry2nd:
    for Y in listofyentry2nd:
        if (X - circlecentre2nd[0]) ** 2 + (Y - circlecentre2nd[1]) ** 2 <= radius ** 2:      # Equation of a circle
            listofentrypoints2nd.append((X, Z, Y))                                 # Saving values that are in the circle

entrypoints2ndsorted = sortList(entry2nd, listofentrypoints2nd)
fullpointslist_2 = []
edgeline1_2 = np.array([7.865108013153076,-21.51528869801447,-78.40716837606037])
edgeline2_2 = np.array([7.865108013153076,-15.372742899197895,-102.29484648256924])

for i in entrypoints2ndsorted:
    # Find equation of line that is n degrees to the long axis
    mLA_2 = (long1[2] - long2[2]) / (long1[1] - long2[1])
    cLA_2 = long1[2] - (mLA_2 * long1[1])

    # Using tan a = (m1 - m2)/(1 + m1m2) to get gradient of k wire    
    m_2 = (mLA_2 - 1) / (mLA_2 + 1)
    c_2 = i[2] - (m_2 * i[1])
    
    # Calculate equation of the edge of the bone
    medge_2 = (edgeline1_2[2] - edgeline2_2[2]) / (edgeline1_2[1] - edgeline2_2[1])
    cedge_2 = edgeline1_2[2] - (medge_2 * edgeline1_2[1])
    
    # Calculate the intersection of the edge of the bone and the wire to find end point
    yexit_2 = (c_2 - cedge_2) / (medge_2 - m_2)
    zexit_2 = (medge_2 * yexit_2) + cedge_2
    
    exitpoint_2 = (i[0], yexit_2, zexit_2)    
    
    # Check that the line calculated crosses the fracture plane
    crossesPlane_2 = checkCrossesPlane(fracture_plane, i, exitpoint_2)
    
    if crossesPlane_2 == False:
        continue
    
    # Save start point and end point
    fullpointslist_2.append([i, exitpoint_2])
    


# =============================================================================
# Third k-wire
# =============================================================================
# Coordinates of distal dorsal of radius
entry3rd = np.array([E3_R,E3_A,E3_S]).astype(float)


cuboid_points_tocheck3 = []

# Approx values
# Define the length of the cuboid relative to the start point
cuboid_length_min3 = entry3rd[0] - 10
cuboid_length_max3 = entry3rd[0] + 10

# Define the width of the cuboid relative to the start point
cuboid_width_max3 = entry3rd[1] + 1
cuboid_width_min3 = entry3rd[1] - 1

# Define the height of the cuboid relative to the start point
cuboid_height_max3 = entry3rd[2] + 2
cuboid_height_min3 = entry3rd[2] - 2

# Use a nested for loop to store all the possible coordinates within the specified range menioned above
# arange() function creates a sequence of numbers that are evenly spaced within a specified range

for x in np.arange(cuboid_length_min3, cuboid_length_max3):
    for y in np.arange(cuboid_width_min3, cuboid_width_max3):
        for z in np.arange(cuboid_height_min3, cuboid_height_max3):
            cuboid_points_tocheck3.append((x, y, z))

cuboid_points3 = []

# Remove any points that are too close to 2nd k wire entry point (within 5mm)
for i in cuboid_points_tocheck3:
    if (i[1] - entry2nd[1])**2 + (i[2] - entry2nd[2])**2 < 5:
        continue
    
    else:
        cuboid_points3.append(i)

# Used to sort entry points by closest to initial chosen value
cuboid_points_sorted_3 = sortList(entry3rd, cuboid_points3)


fullpointslist_3 = []
edgeline1_3 = np.array([10.155582427978516,-24.90958723601122,-75.31703798257502])
edgeline2_3 = np.array([10.155582427978516,-17.14609185139583,-89.30839230210165])

for i in cuboid_points_sorted_3:
    # Calculate equation of the long axis
    mLA_3 = (long1[2] - long2[2]) / (long1[1] - long2[1])
    cLA_3 = long1[2] - (mLA_2 * long1[1])
    
    # Calculate equation of the wire
    m_3 = (mLA_3 - 1) / (mLA_3 + 1)
    c_3 = i[2] - (m_3 * i[1])
    
    # Calculate the equation of the edge
    medge_3 = (edgeline1_3[2] - edgeline2_3[2]) / (edgeline1_3[1] - edgeline2_3[1])
    cedge_3 = edgeline1_3[2] - (medge_3 * edgeline1_3[1])
    
    # Calculate the exit point
    yexit_3 = (c_3 - cedge_3) / (medge_3 - m_3)
    zexit_3 = (medge_3 * yexit_3) + cedge_3
    
    exitpoint_3 = (i[0], yexit_3, zexit_3)    
    
    # Check that the wire crosses the fracture plane
    crossesPlane_3 = checkCrossesPlane(fracture_plane, i, exitpoint_3)
    
    if crossesPlane_3 == False:
        continue
    
 #   print((m_3 - mLA_3) / (1 + (m_3 * mLA_3)))
    
    # Save start point and end point
    fullpointslist_3.append([i, exitpoint_3])


# =============================================================================
# Checking Section
# - no hitting each other
# - no intersections at fracture line
# - no intersections with nerves, arteries etc
# - 3rd k wire cannot have same entry point as 2nd
# =============================================================================
# Code for when 3 wires are chosen
if numberWires == 3:
    workingvalue = False
    
    # Need to iterate through the lists of values. To prevent index errors, iterate through smallest list
    if fullpointslist_1 < fullpointslist_2:
        shortestlist = fullpointslist_1
        
    else:
        shortestlist = fullpointslist_2
    
    if fullpointslist_3 < shortestlist:
        shortestlist = fullpointslist_3  
        
    for i in range(len(shortestlist)):
        # Checking if the lines hit each other
        intersecta = checkIntersect(fullpointslist_1[i], fullpointslist_2[i])
        intersectb = checkIntersect(fullpointslist_1[i], fullpointslist_3[i])
        intersectc = checkIntersect(fullpointslist_2[i], fullpointslist_3[i])
        
        if intersecta == False or intersectb == False or intersectc == False:
            print("Failed 1") # Temporary debug code
            continue
        
        # At this point, the lines do not hit each other
        # Calculate intersection with the fracture plane
        fracturecross1 = crossingPoint(fracture_plane, fullpointslist_1[i][0], fullpointslist_1[i][1])
        fracturecross2 = crossingPoint(fracture_plane, fullpointslist_2[i][0], fullpointslist_2[i][1])
        fracturecross3 = crossingPoint(fracture_plane, fullpointslist_3[i][0], fullpointslist_3[i][1])
        
        # Need to check that the lines dont all cross over at fracture plane - check equation between lines and compare ie. if m12 = m23: they cross so reject
        A = [fracturecross1[0], fracturecross1[1], fracturecross1[2]]
        B = [fracturecross2[0], fracturecross2[1], fracturecross2[2]]
        C = [fracturecross3[0], fracturecross3[1], fracturecross3[2]]
        
        n1 = (A[0] - B[0]) / (B[0] - C[0])
        n2 = (A[1] - B[1]) / (B[1] - C[1])
        n3 = (A[2] - B[2]) / (B[2] - C[2])
        
        if n1 == n2 == n3:
            print("Failed 2") # Temporary debug code
            continue
        
        # Take k wire thickness into account at entry points
        # Find distance between entry points
        point1 = fullpointslist_1[i][0]
        point2 = fullpointslist_2[i][0]
        point3 = fullpointslist_3[i][0]
        
        distance12 = distancePoints(point1, point2)
        distance23 = distancePoints(point2, point3)    
        distance13 = distancePoints(point3, point1)
        
        if distance12 < kWireDiameter or distance13 < kWireDiameter or distance23 < kWireDiameter:
            print("Failed 3") # Temporary debug code
            continue
        
        # At this point, lines are not all crossing at fracture plane
        finalPoints = [fullpointslist_1[i], fullpointslist_2[i], fullpointslist_3[i]]
        workingvalue = True
        
        print("3 wires calculated\n")
        break

# Code to calculate when 2 wires are chosen or 3 wires fail
if numberWires == 2 or workingvalue == False:
    # Iterating through shortest list
    if fullpointslist_1 < fullpointslist_2:
        shortestlist = fullpointslist_1
        
    else:
        shortestlist = fullpointslist_2    
    
    for i in range(len(shortestlist)):
        # Check if the wires intersect
        intersect = checkIntersect(fullpointslist_1[i], fullpointslist_2[i])
        
        if intersect == False:
            print("Failed 4") # Temporary debug code
            continue

        # Take k wire thickness into account at entry points
        # Find distance between entry points
        point1 = fullpointslist_1[i][0]
        point2 = fullpointslist_2[i][0]        
        
        if distance12 < kWireDiameter:
            print("Failed 5") # Temporary debug code
            continue
        
        # At this point, lines are not all crossing at fracture plane
        finalPoints = [fullpointslist_1[i], fullpointslist_2[i]]
        minworkingvalue = True
        
        print("2 Wires calculated\n")
        break
        
# =============================================================================
# Compression Calculation.
# =============================================================================
#entry1st,entry2nd,entry3rd are the ideal entry points for the wires
#finalPointsandlength[1][1] 1st wire actual entry point
#finalPointsandlength[2][1] 2nd wire actual entry point
#finalPointsandlength[3][1] 3rd wire actual entry point do an if statement to check if 3 wires are used
#do pythagoras to find the distance between the ideal entry point and the actual entry point
#subtract it from 5mm
#considerations: need direction of difference, 
#i need to change pointsandlength to real variable name as it isnt defined yet. 

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2+ (p1[2] - p2[2])**2)

def direction_difference(p1, p2):
    if p1[1] > p2[1]:
        return "up"
    elif p1[1] < p2[1]:
        return "down"
    else:
        return "none"

compression_results = []

if len(finalPoints) >= 2:
    entry_points = [entry1st, entry2nd]

    if len(finalPoints) >= 3:
        entry_points.append(entry3rd)
    #might need to adjust positioning a bit.

    for entry in entry_points:
        up_allowable_range = 5
        down_allowable_range = 5
        
        for i, actual_entry in enumerate(finalPoints, start=1):
            distance_difference = 5 - distance(entry, actual_entry[i][1])
            direction = direction_difference(entry, actual_entry[i][1])

            compression_results.append((distance_difference, direction))

            if direction == "up":
                up_allowable_range -= distance_difference
            elif direction == "down":
                down_allowable_range -= distance_difference
        up_allowable_range = max(0, up_allowable_range)
        down_allowable_range = max(0, down_allowable_range)

        print(f"In regards to compression, we can go {up_allowable_range:.2f} mm up and {down_allowable_range:.2f} mm down.")

else:
    print("Error: Not enough wires selected.")



# =============================================================================
# Prepare results
# - length of wire in bone
# =============================================================================
pointsandlength = []

# Create a list of entry, exit and length of wire
for i in finalPoints:
    pointsandlength.append((i[0], i[1], distancePoints(i[0], i[1])))

# Preparing headings for the csv file
finalPointsandlength = [["K wire number", "Entry point", "Exit point", "Length"]]
wirenumber = 1


for i in pointsandlength:
    """ May need to use this if Solidworks is misbehaving
    Yfentry, Zfentry = swapYZ(i[0][1], i[0][2])
    entryP = (i[0][0], Yfentry, Zfentry)
    
    Yfexit, Zfexit = swapYZ(i[1][1], i[1][2])
    exitP = (i[1][0], Yfexit, Zfexit)
    
    finalPointsandlength.append([wirenumber, entryP, exitP, i[2]])
    
    wirenumber += 1
    """
    
    finalPointsandlength.append([wirenumber, i[0], i[1], i[2]])
    wirenumber += 1

# Print final chosen values    
print("K wire 1 entry: {}".format(finalPointsandlength[1][1]))
print("K wire 1 exit: {}".format(finalPointsandlength[1][2]))
print("K wire 1 length: {}\n".format(finalPointsandlength[1][3]))

print("K wire 2 entry: {}".format(finalPointsandlength[2][1]))
print("K wire 2 exit: {}".format(finalPointsandlength[2][2]))
print("K wire 2 length: {}\n".format(finalPointsandlength[2][3]))

if numberWires == 3 and workingvalue == False:
    print("A third wire could not be calculated")
    
elif numberWires == 3:
    print("K wire 3 entry: {}".format(finalPointsandlength[3][1]))
    print("K wire 3 exit: {}".format(finalPointsandlength[3][2]))
    print("K wire 3 length: {}\n".format(finalPointsandlength[3][3]))

# Save values as a csv file
header = ["K wire number", "Entry point", "Exit point", "Length"]

file_path = askdirectory()
os.chdir(file_path)
	    
with open('wireinfo.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(finalPointsandlength)
