from math import sqrt
import sympy


def lic_0_check(data_points, length1):
    """Function for checking requirement LIC 0. Returns True
    if there exists 2 consecutive points with a distance
    larger than length1, False otherwise."""
    if len(data_points) < 2:
        return False
    for index in range(len(data_points)-1):
        (x_1, y_1) = data_points[index]
        (x_2, y_2) = data_points[index + 1]
        dist = sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2)
        if dist > length1:
            return True
    return False


def lic_1_check(data_points, radius1):
    """Function for checking requirement LIC 1. Returns True
    if there exists 3 consecutive points that cannot fit within
    a circle of radius radius1, False otherwise.
    """
    if len(data_points) < 3:
        return False
    for index in range(len(data_points) - 2):
        [(x_1, y_1), (x_2, y_2), (x_3, y_3)] = (data_points[index], data_points[index + 1], data_points[index + 2])
        distAB = sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2) > 2*radius1
        distAC = sqrt((x_3 - x_1)**2 + (y_3 - y_1)**2) > 2*radius1
        distBC = sqrt((x_3 - x_2)**2 + (y_3 - y_2)**2) > 2*radius1
        if distAB or distAC or distBC:
            return True
        midpoints = [((x_1 + x_2)/2, (y_1 + y_2)/2),
                     ((x_1 + x_3)/2, (y_1 + y_3)/2),
                     ((x_2 + x_3)/2, (y_2 + y_3)/2)]
        k_values = [(y_2 - y_1)/(x_2 - x_1) if x_1 != x_2 else None,
                  (y_3 - y_1)/(x_3 - x_1) if x_1 != x_3 else None,
                  (y_3 - y_2)/(x_3 - x_2) if x_2 != x_3 else None]
        if k_values[0] == k_values[1] == k_values[2]:
            continue
        equations = []
        x, y = sympy.symbols('x y')
        for slope, coord in zip(k_values, midpoints):
            if slope == 0:
                pass
            elif slope is None:
                equation = sympy.Eq(y - coord[1], 0)
                equations.append(equation)
            else:
                equation = sympy.Eq(y - coord[1], -(1/slope)*(x - coord[0]))
                equations.append(equation)
        circumcenter = sympy.solve((equations[0], equations[1]), (x, y))
        if sqrt((circumcenter[x] - x_1)**2 + (circumcenter[y] - y_1)**2) > radius1:
            return True
    return False
