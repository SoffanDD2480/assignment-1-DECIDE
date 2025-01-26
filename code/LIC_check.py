from math import sqrt, acos, pi


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

def lic_2_check (data_points, epsilon):
    """function that checks the LIC 2. Returns True if there exists at least one set 
        of three consecutive data points which form an angle such that the angle is:
        less than pi - epsilon
        greater than pi + epsilon.
    """
   
    for i in range (len(data_points) -2):
        p1,p2,p3 = data_points[i], data_points[i+1], data_points[i+2]
        angle = calculate_angle(p1,p2,p3)

        if(angle == None):
            continue

        if(angle < (pi - epsilon) or angle > (pi + epsilon)):
            return True
    return False


def lic_3_check (data_points, area1):
    """function that checks the LIC 3. Returns True if there exists at least one set
    of three consecutive data points which form a triangle with area greater than area1.
    """
    for i in range(len(data_points) - 2):
        p1,p2,p3 = data_points[i], data_points[i+1], data_points[i+2]
        area = 0.5 * abs((p1[0] - p3[0]) * (p2[1] - p1[1]) - (p1[0] - p2[0]) * (p3[1] - p1[1]))
        
        """if the area is 0, the points are aligned"""
        if area == 0:
            continue

        if area > area1:
            return True
    return False

def lic_5_check(data_points):
    """ function that check the LIC 5. Returns True if there exists at least one set of two consecutive data points,
    (x[i],y[i]) and (x[j],y[j]), such that x[j] - x[i] < 0.
    """
    for i in range(len(data_points) - 1):
        x_i = data_points[i]
        x_j = data_points[i+1]

        if x_j[0] - x_i[0] < 0:
            return True
        
    return False

