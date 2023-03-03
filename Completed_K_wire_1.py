import numpy as np
import cv2 


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

# Create ROI of other potential points


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