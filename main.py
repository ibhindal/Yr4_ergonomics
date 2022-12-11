# =============================================================================
# Notes for this
# Changing entry point to begin with, assuming the angle is the same (45 deg), if time permitted, angle can be changed
# Coordinates in 3D Slicer are in RAS System
# =============================================================================

# After input, confirm the input
# Change the written input to click boxes

#import slicer
import numpy as np
import matplotlib.pyplot as plt
import math
import cv2


# Setting up k-wire information
# Left or right hand will potentially make a difference in some of the code: left = 0, right = 1
handInput = input("Is this the left or right hand?")
if handInput.lower() == "left" or handInput.lower() == "l":
    handSide = 0
    print("Your arm is the left one")
    
elif handInput.lower() == "right" or handInput.lower() == "r":
    handSide = 1
    print("Your arm is the right one")

angleofentry = 45


# User can input a k-wire thickness or type x which chooses the average value for them
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

# =============================================================================
# ask the user to choose 3 points to define the fracture plane
# =============================================================================
fracturecoord1 = np.array([1, 1, 1])
fracturecoord2 = np.array([2, 2, 2])
fracturecoord3 = np.array([3, 3, 3])

# Calculate normal vector of fracture plane
vector1 = fracturecoord2 - fracturecoord1
vector2 = fracturecoord3 - fracturecoord1
normal = np.cross(vector1, vector2)
a=normal[0]
b=normal[1]
c=normal[2]
# create a new vector from the normal and any of the original points
 # and use it to find the d coefficient of the plane
d = -np.dot(normal, fracturecoord1)

fracture_plane = [a, b, c, d]  # plane equation: a*x + b*y + c*z + d = 0
#for the above  a, b and c are the simplified normal vector and d is if you sub in any of the fracture coordinates
#into the plane equation and equate to zero


#THIS NEEDS LIMITS TO HOW BIG TO MAKE IT.

# =============================================================================
# Functions - may be needed multiple times so include here
# =============================================================================

# Edge detection algorithm - creates the edges and stores as an image, last 2 lines get the coordinates of the edges (increasing in x value)
def simple_edge_detection(image): 
   edges_detected = cv2.Canny(image , 100, 200) 
   images = [image , edges_detected]

   location = [121, 122] 
   for loc, edge_image in zip(location, images): 
     plt.subplot(loc) 
     plt.imshow(edge_image, cmap='gray')

   cv2.imwrite('edge_detected.png', edges_detected) 
   plt.savefig('edge_plot.png') 
   plt.show()
   
   indices = np.where(edges_detected != [0])
   coordinates = list(zip(indices[0], indices[1]))

   return coordinates

def RAStoXYZ():
    pass


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
# Code to select centre of Lister's tubercle
coordinatesListers = np.array([-8,42,-80]) # Random numbers for now - will be taken from 3D Slicer
radius = 3 # Average radius (may not work)
centreRS = (coordinatesListers[0], coordinatesListers[2])

"""Need function to convert RAS to python here"""


# Finding x and y values that are within the Lister's Tubercle to trial entry points - using a circle as a model

minR = centreRS[0] - radius
maxR = centreRS[0] + radius
minS = centreRS[1] - radius
maxS = centreRS[1] + radius

listofRvalues = np.arange(minR, maxR + 1, 1) # Creating a selection of x values that are 0.5 apart
listofSvalues = np.arange(minS, maxS + 1, 1) # Creating a selection of y values that are 0.5 apart

listofentrypoints = [] # Create a list of coordinates that are within our Lister's tubercle circle
A = coordinatesListers[1]

for R in listofRvalues:
    for S in listofSvalues:
        if (R - centreRS[0]) ** 2 + (S - centreRS[1]) ** 2 <= radius ** 2: # Equation of a circle
            listofentrypoints.append((R, A, S))
         
# Determine long axis - currently selecting 2 points on sagittal view
point1 = (-8,16,-71)
point2 = (6,15,-128)

# Equation of straight line - potentially temporary code
m = (point2[2] - point1[2]) / (point2[1] - point1[1]) # Only need to know A and S as R wont change across k-wire
c = point1[2] - m * point1[1]

#print("Bone axis equation: S = {}A + {}".format(m, c))

# Calculate equation of each k-wire line
if m == float(-1):
    print("Please try again with slightly different points") # Is there a way to go back to selecting 2 points?

tanAngle = math.tan(angleofentry * math.pi / 180)

mkwire = (m - tanAngle) / (m * tanAngle + 1) # Gradient of k-wire: This value will need to go in a for loop when the angle gets changed
ckwire = []

for i in listofentrypoints:    # Equation of line at each entry point
    ckwire.append(i[2] - mkwire * i[1])
    
    #print("K wire equation: S = {}A + {}, R = {}".format(mkwire, ckwire[-1], coordinatesListers[0])) # Prints equation of k wire and the plane it should be in
    
# Edge detection of image
img = cv2.imread('Kwire2Image.jpg', 0)
edges2nd = simple_edge_detection(img)


# This next bit will vary for left and right side
# Calculating skin entry points

"""Not currently working as 3d slicer coordinates are different to python"""
if handSide == 0:
    successfulValues = 0
    
    for kwire in ckwire: # For each potential k wire
        testAedge = int(A + 1) # Going along the A axis (image x axis)
        keepGoing = 0
        
        
        while keepGoing == 0:
            
            SofTestA = mkwire * testAedge + kwire # Calculate S for each A
            coordsTestValue = (testAedge, SofTestA) 
            
            
            if coordsTestValue in edges2nd: # Testing if the calculated coords from the line are equal to any coords from edge detection
                entryPoint = (coordinatesListers[0], testAedge, SofTestA)
                
                keepGoing = 1
            
            if testAedge > A + 100:
                keepGoing = 1
            
            testAedge += 1
        
        if keepGoing == 0:
            successfulValues += 1
    
    print("Successful kwire trajectories = {}".format(successfulValues))
    
    """ In theory k wire 2 is done
    Current problems (and potential solutions):
        - May not return a value because of rounding errors - solve by finding nearest?
        - Coordinates not the same in 3D slicer and python - need to create a function to convert
        - Image coordinates may vary depending on how the image is take - save view as image rather than screenshot
        - No values from 3D slicer - use mark up to select lister's tubercle in 3D, bring A-S view to that and then save image, repeat with long axis calculation
    
    
    
    """
    
elif handSide == 1: # Same code but opposite direction
    pass

# =============================================================================
# Third k-wire
# =============================================================================




# =============================================================================
# Checking Section
# - no intersections at fracture line
# - no intersections with nerves, arteries etc
# =============================================================================


# =============================================================================
# Preview image
# =============================================================================
