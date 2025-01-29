from math import sqrt, acos, pi, fabs
from sympy import Eq, solve, symbols


def calculate_distance(p1, p2):
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def calculate_triangle_area(p1, p2, p3) -> float:
    """
    Calculate the area of a triangle given three points.

    Uses following formula:
    1/2 |x_1(y_2 - y_3) + x_2(y_3 - y_1) + x_3(y_1 - y_2)|
    """
    area = 0.5 * fabs(
        (p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1]))
    )
    return area


def calculate_circumcenter(p1, p2, p3):
    """Calculate circumcenter of triangle.
    Returns coordinates of circumcenter,
    otherwise None if input is not a triangle"""
    (x_1, y_1), (x_2, y_2), (x_3, y_3) = p1, p2, p3
    midpoints = [
        ((x_1 + x_2) / 2, (y_1 + y_2) / 2),
        ((x_1 + x_3) / 2, (y_1 + y_3) / 2),
        ((x_2 + x_3) / 2, (y_2 + y_3) / 2),
    ]
    if (
        midpoints[0] in midpoints[1:] or midpoints[1] == midpoints[2]
    ):  # Check if any points coincide
        return None
    k_values = [
        (y_2 - y_1) / (x_2 - x_1) if x_1 != x_2 else None,
        (y_3 - y_1) / (x_3 - x_1) if x_1 != x_3 else None,
        (y_3 - y_2) / (x_3 - x_2) if x_2 != x_3 else None,
    ]
    if (
        k_values[0] == k_values[1] == k_values[2]
    ):  # Colinearity check ==> no circumcenter
        return None
    equations = []
    x, y = symbols("x y")
    for slope, coord in zip(k_values, midpoints):
        if slope == 0:
            pass
        elif slope is None:
            equation = Eq(y - coord[1], 0)
            equations.append(equation)
        else:
            equation = Eq(y - coord[1], -(1 / slope) * (x - coord[0]))
            equations.append(equation)
    circumcenter = solve((equations[0], equations[1]), (x, y))
    to_tuple = (circumcenter[x], circumcenter[y])
    return to_tuple


def calculate_angle(p1, p2, p3):
    """function that allows to calculate the angle given the three point.
    The second point is the vertex of the angle
    This function is used for calculate LIC 2."""
    v1 = (p1[0] - p2[0], p1[1] - p2[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])

    scalar_product = v1[0] * v2[0] + v1[1] * v2[1]
    norm_v1 = sqrt(v1[0] ** 2 + v1[1] ** 2)
    norm_v2 = sqrt(v2[0] ** 2 + v2[1] ** 2)

    if norm_v1 == 0 or norm_v2 == 0:
        return None

    cos_angle = scalar_product / (norm_v1 * norm_v2)
    angle = acos(cos_angle)
    return angle
