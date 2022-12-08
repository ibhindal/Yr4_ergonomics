import cv2

# Load the 3D model from a file
model = cv2.imread('model.png')

# Define the starting and ending points of the line
start_point = (10, 10)
end_point = (100, 100)

# Draw a line of thickness 3 on the 3D model
model = cv2.line(model, start_point, end_point, (255, 0, 0), 3)

# Save the modified 3D model to a file
cv2.imwrite('modified_model.png', model)
