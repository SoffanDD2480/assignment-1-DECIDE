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

def lic_4_check (data_points, q_pts, quads):
    """function that checks the LIC 4. Returns True if there exists at least one set
    of q_pts consecutive data points that lie in more than quads quadrants.
    """

    if q_pts <= 0 or len(data_points) < q_pts:
        return False

    for i in range(len(data_points) - q_pts + 1):
        quadrants = set()
        for j in range(i, i + q_pts):
            x,y = data_points[j]
            if x >= 0 and y >= 0:
                quadrants.add(1)
            elif x < 0 and y > 0:
                quadrants.add(2)
            elif x < 0 and y < 0:
                quadrants.add(3)
            elif x > 0 and y < 0:
                quadrants.add(4)

        if len(quadrants) > quads:
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

def lic_6_check(data_points, dist, n_pts):
    """function that check the LIC 6. Returns True if there exists at least one set of n_pts consecutive data points
    such that at least one of the point lies a distance greater than dist from the line joining the first and last of these n_pts points.
    If the first and last points of these N PTS are identical, then the calculated distance 
    to compare with DIST will be the distance from the coincident point to all other points of
    the N PTS consecutive points. The condition is not met when NUMPOINTS < 3.
    """

    if (len(data_points) < 3) or (n_pts > len(data_points)) or (dist < 0):
        return False

    for i in range(len(data_points) - n_pts + 1):
        p1 = data_points[i]
        p2 = data_points[i + n_pts - 1]

        if p1 == p2:
            for j in range(i + 1, i + n_pts - 1):
                p = data_points[j]
                distance_calculated = sqrt((p[0] - p1[0])**2 + (p[1] - p1[1])**2)
                if distance_calculated > dist:
                    return True
                
        else:
            for j in range(i + 1, i + n_pts - 1):
                p = data_points[j]
                distance_calculated = abs((p2[0] - p1[0]) * (p1[1] - p[1]) - (p1[0] - p[0]) * (p2[1] - p1[1])) / sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
                if distance_calculated > dist:
                    return True
                
    return False




                

    
       


