xy_dict = {"min_x": -5,
           "max_x":  5,
           "min_y": -5,
           "max_y":  5}

minimum = (1, 3)


def f(x: float, y: float) -> float:
    """
    Return the value of the function f for the given x and y.
    
    z = f(x, y) = 5*(x**2) + 5*(y**2) + 8*x*y - 34*x - 38*y + 74
    
    Input:
     - x: float
     - y: float
    Output:
     - z: float
    """
    return 5*(x**2) + 5*(y**2) + 8*x*y - 34*x - 38*y + 74


def f_x(x: float, y: float) -> float:
    """
    Return the value of the derivative of the f function
    of a variable x for the given x and y.
    
    f(x, y) = 5*(x**2) + 5*(y**2) + 8*x*y - 34*x - 38*y + 74
    z = fx(x, y) = 10*x + 8*y - 34
    
    Input:
     - x: float
     - y: float
    Output:
     - z: float
    """
    return 10*x + 8*y - 34


def f_y(x: float, y: float) -> float:
    """
    Return the value of the derivative of the f function
    of a variable y for the given x and y.
    
    f(x, y) = 5*(x**2) + 5*(y**2) + 8*x*y - 34*x - 38*y + 74
    z = fy(x, y) = 10*y + 8*x - 38
    
    Input:
     - x: float
     - y: float
    Output:
     - z: float
    """
    return 10*y + 8*x - 38


def gradient(x: float, y: float) -> list:#[float]:
    """
    Return the gradient of the function for the given x and y.

    f(x, y)  = 5*(x**2) + 5*(y**2) + 8*x*y - 34*x - 38*y + 74
    fx(x, y) = 10*x + 8*y - 34
    fy(x, y) = 10*y + 8*x - 38
    gradient = [fx(x, y), fy(x, y)]
    
    Input:
     - x: float
     - y: float
    Output:
     - gradient: list[float]
    """
    return [f_x(x, y), f_y(x, y)]


def correct(x: float, y: float, x_y: dict) -> tuple:#[float]
    """
    Return corrected x and y.
    When a parameter exceeds the boundary value,
    it sets it to the boundary value.

    Input:
     - x: float
     - y: float
    Output:
     - x: float
     - y: float
    """
    if x < x_y["min_x"]:
        x = x_y["min_x"]
    elif x > x_y["max_x"]:
        x = x_y["max_x"]
    
    if y < x_y["min_y"]:
        y = x_y["min_y"]
    elif y > x_y["max_x"]:
        y = x_y["max_x"]
    return x, y


def hesjan():
    """
    Return the hesjan of f function.    

    Output:
     - hesjan: list[list][float]
    """
    return [[5/18, -2/9],
            [-2/9, 5/18]]


def mul_matrices(m2x2: list, m1x2: list) -> list:
    """
    Return a new matrix created by mul matrix 2x2 (hesjan)
    and matrix 1x2 (gradient).
    A new matrix is 1x2 as gradient.

    Input:
     - m2x2: list[list][float] - hesjan
     - m1x2: list[float] - gradient
    Output:
     - matrix: list[float]
    """
    result = [[0], [0]]
    m1x2 = [[row] for row in m1x2]
    for i in range(len(m2x2)):
       for j in range(len(m1x2[0])):
           for k in range(len(m1x2)):
               result[i][j] += m2x2[i][k] * m1x2[k][j]
    return [row[0] for row in result]

