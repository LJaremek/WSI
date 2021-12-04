from logic import gradient, hesjan, mul_matrices
from plot import *

# Parameters
B = 0.5
epsilon = 0.1

# Title
plt.title(f"""f(x, y) = 5*(x**2) + 5*(y**2) + 8*x*y - 34*x - 38*y + 74\n
B = {B}, epsilon={epsilon}\n""")

# Start point
x = uniform(min_x, max_x)
y = uniform(min_y, max_y)
ax.add_patch(plt.Circle((x, y), 0.05, color="yellow"))
stop = False

# Hesjan loop
while not stop:
    grad = gradient(x, y)
    h_x, h_y = mul_matrices(hesjan(), grad)
    x -= h_x*B
    y -= h_y*B
    ax.add_patch(plt.Circle((x, y), 0.05, color="white"))
    stop = ( (x - end_x)**2 + (y - end_y)**2 )**(1/2) < epsilon

# Exact minimum point
ax.add_patch(plt.Circle(minimum, 0.02, color="red", fill=False))

plt.show()

