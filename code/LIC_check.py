from math import sqrt, sin, acos


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

    Not finished, circumcenter implementation needed.
    """
    if len(data_points) < 3:
        return False
    for index in range(len(data_points) - 2):
        (x_1, y_1), (x_2, y_2), (x_3, y_3) = data_points[index], data_points[index + 1], data_points[index + 2]
        dist1 = sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2) > 2*radius1
        dist2 = sqrt((x_3 - x_1)**2 + (y_3 - y_1)**2) > 2*radius1
        dist3 = sqrt((x_3 - x_2)**2 + (y_3 - y_2)**2) > 2*radius1
        if dist1 or dist2 or dist3:
            return True
        



def calculate_angle(p1,p2,p3):
    """function that allows to calculate the angle given the three point.
    The second point is the vertex of the angle
    This function is used for calculate LIC 2."""
    v1 = ((p1[0] - p2[0], p1[1] - p2[1]))
    v2 = ((p3[0] - p2[0], p3[1] - p2[1]))

    scalar_product = v1[0] * v2[0] + v1[1] * v2[1]
    norm_v1 = sqrt(v1[0]**2 + v1[1]**2)
    norm_v2 = sqrt(v2[0]**2 + v2[1]**2)

    if norm_v1 == 0 or norm_v2 == 0:
        return  None
    
    cos_angle = scalar_product / (norm_v1 * norm_v2)
    angle = acos (cos_angle)
    return angle

