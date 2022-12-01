#Ibrahim's trial file. please ignore this file or don't I'm not in charge of you


# =============================================================================
# Notes for this
# Changing entry point to begin with, assuming the angle is the same (45 deg), if time permitted, angle can be changed
# Coordinates in 3D Slicer are in RAS System
# =============================================================================

#import slicer
import numpy as np
import matplotlib.pyplot as plt
import math
import cv2 # Need to pip install opencv-python


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
# 
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




# =============================================================================
# First k-wire
# =============================================================================
radiusof1 = 3 # Average radius (may not work)

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

## mask of green (36,25,25) ~ (86, 255,255)
# mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))

## slice the green
imask = mask>0
green = np.zeros_like(img, np.uint8)
green[imask] = img[imask]

points = cv2.findNonZero(mask)
avg = np.mean(points, axis=0)
# assuming the resolutions of the image and screen are the following
resImage = [640, 480] #change when have image resolution
resScreen = [1920, 1080]



# points are in x,y coordinates
pointInScreen = ((resScreen[0] / resImage[0]) * avg[0], (resScreen[1] / resImage[1]) * avg[1] )
centreRSof1=pointInScreen
minR = centreRSof1[0] - radiusof1
maxR = centreRSof1[0] + radiusof1
minS = centreRSof1[1] - radiusof1
maxS = centreRSof1[1] + radiusof1

listofRvaluesof1 = np.arange(minR, maxR + 1, 1) # Creating a selection of x values that are 0.5 apart
listofSvaluesof1 = np.arange(minS, maxS + 1, 1) # Creating a selection of y values that are 0.5 apart

listofentrypoints = [] # Create a list of coordinates that are within our Lister's tubercle circle
A = 





point1of1=pointInScreen

point2of1= [] #change this to a point where you want it to go

# Equation of straight line - potentially temporary code
m = (point2of1[2] - point1of1[2]) / (point2of1[1] - point1of1[1]) # Only need to know A and S as R wont change across k-wire
c = point1of1[2] - m * point1of1[1]

print("Bone axis equation: S = {}A + {}".format(m, c))

# Calculate equation of each k-wire line
if m == float(-1):
    print("Please try again with slightly different points") # Is there a way to go back to selecting 2 points?

tanAngle = math.tan(angleofentry * math.pi / 180)

mkwire = (m - tanAngle) / (m * tanAngle + 1) # Gradient of k-wire: This value will need to go in a for loop when the angle gets changed
ckwire = []

for i in listofentrypoints:    # Equation of line at each entry point
    ckwire.append(i[2] - mkwire * i[1])
    
    print("K wire equation: S = {}A + {}, R = {}".format(mkwire, ckwire[-1], coordinatesListers[0])) # Prints equation of k wire and the plane it should be in
    
# Edge detection of image
img = cv2.imread('Kwire2Image.jpg', 0)
edges2nd = simple_edge_detection(img)




# =============================================================================
# Second k-wire
# =============================================================================
# Code to select centre of Lister's tubercle
coordinatesListers = np.array([-8,3,-80]) # Random numbers for now - will be taken from 3D Slicer
radius = 3 # Average radius (may not work)
centreRS = (coordinatesListers[0], coordinatesListers[2])

# Draw a circle on the image of Lister's tubercle - representing the area that the k-wire can enter - 2D
# Other options - get user to select 2 ends and create circle from that - simultaneous equations
"""
fig, ax = plt.subplots()
ax.add_patch(plt.Circle(centreRS, radius, fill = False))

ax.set_aspect('equal', adjustable='datalim')
ax.plot()   
plt.show()"""

# Finding x and y values that are within the Lister's Tubercle to trial entry points

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

print("Bone axis equation: S = {}A + {}".format(m, c))

# Calculate equation of each k-wire line
if m == float(-1):
    print("Please try again with slightly different points") # Is there a way to go back to selecting 2 points?

tanAngle = math.tan(angleofentry * math.pi / 180)

mkwire = (m - tanAngle) / (m * tanAngle + 1) # Gradient of k-wire: This value will need to go in a for loop when the angle gets changed
ckwire = []

for i in listofentrypoints:    # Equation of line at each entry point
    ckwire.append(i[2] - mkwire * i[1])
    
    print("K wire equation: S = {}A + {}, R = {}".format(mkwire, ckwire[-1], coordinatesListers[0])) # Prints equation of k wire and the plane it should be in
    
# Edge detection of image
img = cv2.imread('Kwire2Image.jpg', 0)
edges2nd = simple_edge_detection(img)

######### At this point, it may be best to compare to anatomy and rule out some values

# This next bit will vary for left and right side
# Calculating skin entry points
if handSide == 0:
    for kwire in range(len(ckwire)):
        startingAvalue = A + 1
        
        
    
    
    
    
    
    
    
    
elif handSide == 1:
    pass

# =============================================================================
# Third k-wire
# =============================================================================




# =============================================================================
# Checking Section
# - no intersections at fracture line
# - no intersections with nerves, arteries etc
# =============================================================================
#code that detects the colour red
if

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if img[i,j,0]<10 and img[i,j,1]<10 and img[i,j,2]>220:
            img[i,j,0]=0
            img[i,j,1]=0
            img[i,j,2]=255
            coord.append([i,j])
        else:
            img[i,j,0]=0
            img[i,j,1]=0
            img[i,j,2]=0

for l in range(len(coord)):
    px=coord[l][0]
    py=coord[l][1]
    cv2.circle(img,(py,px),5,(0,255,255),1)


# =============================================================================
# Other
# - convert RAS to XYZ
# - extend line to skin rather than bone
# =============================================================================
