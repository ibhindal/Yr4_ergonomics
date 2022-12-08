import matplotlib.pyplot as plt
import matplotlib.patches as patches



# Create a figure and set the limits for the x and y axes
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Create a box at the origin with width 5 and height 10
rect = plt.Rectangle((0, 0), 5, 10)
ax.add_patch(rect)

# Show the plot
plt.show()


# Get the coordinates of the lower-left corner of the box
lower_left = rect.xy
print(f'Lower-left corner: {lower_left}')

# Get the coordinates of the upper-right corner of the box
upper_right = (rect.get_x() + rect.get_width(), rect.get_y() + rect.get_height())
print(f'Upper-right corner: {upper_right}')





# Draw a circle at the center of the box
circle = patches.Circle((rect.get_x() + rect.get_width() / 2, rect.get_y() + rect.get_height() / 2), 1)
ax.add_patch(circle)

# Draw a circle at the top-left corner of the box
circle = patches.Circle((rect.get_x(), rect.get_y() + rect.get_height()), 1)
ax.add_patch(circle)

# Draw a circle at the top-right corner of the box
circle = patches.Circle((rect.get_x() + rect.get_width(), rect.get_y() + rect.get_height()), 1)
ax.add_patch(circle)

# Show the plot
plt.show()


