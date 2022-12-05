# =============================================================================
# Notes for this
# Changing entry point to begin with, assuming the angle is the same (45 deg), if time permitted, angle can be changed
# Coordinates in 3D Slicer are in RAS System
# =============================================================================

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


