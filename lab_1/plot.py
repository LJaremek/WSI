from random import uniform

from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt

from logic import f, f_x, f_y
from logic import xy_dict, minimum

min_x = xy_dict["min_x"]
max_x = xy_dict["max_x"]
min_y = xy_dict["min_y"]
max_y = xy_dict["max_y"]

end_x = minimum[0]
end_y = minimum[1]

X_list = [n/10 for n in range(10*(min_x-1), 10*(max_x+1)+1)]
Y_list = [n/10 for n in range(10*(min_x-1), 10*(max_x+1)+1)]
Z_list = []
for x in X_list:
    row = []
    for y in Y_list:
        row.append(f(x, y))
    Z_list.append(row)

# Drawing colour map and contours
pc = plt.pcolormesh(X_list, Y_list, Z_list)
plt.contour(X_list, Y_list, gaussian_filter(Z_list, .1), 20, colors='k')

# Setting up the plot
ax = plt.gca()
ax.set_xlim((min_x, max_x))
ax.set_ylim((min_y, max_y))
plt.xticks(range(min_x, max_x+1))
plt.yticks(range(min_y, max_y+1))

#   x axis
ax.set_xlabel("x")

#   y axis
y_label = plt.ylabel("y")
y_label.set_rotation(0)

#   z axis
cbar = plt.colorbar(pc)
cbar.set_label("z = f(x, y)", rotation=0, labelpad = 30)

# The surroundings of the minimum point
ax.add_patch(plt.Circle(minimum, 0.4, color="red", fill=False))

