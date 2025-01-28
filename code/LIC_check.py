from math import sqrt, acos, pi, fabs
from sympy import Eq, solve, symbols


def calculate_distance(p1, p2):
    return sqrt(fabs(p2[0] - p1[0]) ** 2 + fabs(p2[1] - p1[1]) ** 2)


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
    midpoints = [((x_1 + x_2) / 2, (y_1 + y_2) / 2),
                 ((x_1 + x_3) / 2, (y_1 + y_3) / 2),
                 ((x_2 + x_3) / 2, (y_2 + y_3) / 2)]
    if midpoints[0] in midpoints[1:] or midpoints[1] == midpoints[2]:  # Check if any points coincide
        return None
    k_values = [(y_2 - y_1) / (x_2 - x_1) if x_1 != x_2 else None,
                (y_3 - y_1) / (x_3 - x_1) if x_1 != x_3 else None,
                (y_3 - y_2) / (x_3 - x_2) if x_2 != x_3 else None]
    if k_values[0] == k_values[1] == k_values[2]:  # Colinearity check ==> no circumcenter
        return None
    equations = []
    x, y = symbols('x y')
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


def lic_0_check(data_points, length1):
    """Function for checking requirement LIC 0. Returns True
    if there exists 2 consecutive points with a distance
    larger than length1, False otherwise."""
    if len(data_points) < 2:
        return False
    for index in range(len(data_points) - 1):
        p1 = data_points[index]
        p2 = data_points[index + 1]
        dist = calculate_distance(p1, p2)
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
        p1, p2, p3 = (data_points[index],
                      data_points[index + 1],
                      data_points[index + 2])
        dist1 = calculate_distance(p1, p2) > 2 * radius1
        dist2 = calculate_distance(p1, p3) > 2 * radius1
        dist3 = calculate_distance(p2, p3) > 2 * radius1
        if dist1 or dist2 or dist3:
            return True
        circumcenter = calculate_circumcenter(p1, p2, p3)
        if circumcenter is None:
            continue
        if calculate_distance(circumcenter, p1) > radius1:
            return True
    return False


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


def lic_2_check(data_points, epsilon):
    """function that checks the LIC 2. Returns True if there exists at least one set
    of three consecutive data points which form an angle such that the angle is:
    less than pi - epsilon
    greater than pi + epsilon.
    """

    for i in range(len(data_points) - 2):
        p1, p2, p3 = data_points[i], data_points[i + 1], data_points[i + 2]
        angle = calculate_angle(p1, p2, p3)

        if angle == None:
            continue

        if angle < (pi - epsilon) or angle > (pi + epsilon):
            return True
    return False


def lic_3_check(data_points, area1):
    """function that checks the LIC 3. Returns True if there exists at least one set
    of three consecutive data points which form a triangle with area greater than area1.
    """
    for i in range(len(data_points) - 2):
        p1, p2, p3 = data_points[i], data_points[i + 1], data_points[i + 2]
        area = calculate_triangle_area(p1, p2, p3)

        """if the area is 0, the points are aligned"""
        if area == 0:
            continue

        if area > area1:
            return True
    return False


def lic_4_check(data_points, q_pts, quads):
    """function that checks the LIC 4. Returns True if there exists at least one set
    of q_pts consecutive data points that lie in more than quads quadrants.
    """

    if q_pts <= 0 or len(data_points) < q_pts:
        return False

    for i in range(len(data_points) - q_pts + 1):
        quadrants = set()
        for j in range(i, i + q_pts):
            x, y = data_points[j]
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
    """function that check the LIC 5. Returns True if there exists at least one set of two consecutive data points,
    (x[i],y[i]) and (x[j],y[j]), such that x[j] - x[i] < 0.
    """
    for i in range(len(data_points) - 1):
        x_i = data_points[i]
        x_j = data_points[i + 1]

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
                distance_calculated = calculate_distance(p1, p)
                if distance_calculated > dist:
                    return True
                
        else:
            for j in range(i + 1, i + n_pts - 1):
                p = data_points[j]
                distance_calculated = abs((p2[0] - p1[0]) * (p1[1] - p[1]) - (p1[0] - p[0]) * (p2[1] - p1[1])) / sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
                if distance_calculated > dist:
                    return True
                
    return False


def lic_7_check(data_points, k_pts, length1):
    """Function for checking requirement LIC 7. Returns True
    if there exists 2 points, K_PTS consecutive interveining
    points apart with distance LENGTH1 between them, False
    otherwise.
    """
    if len(data_points) < 3 or len(data_points)-2 < k_pts:
        return False
    for index in range(len(data_points) - k_pts - 1):
        p1 = data_points[index]
        p2 = data_points[index + k_pts + 1]
        distance = calculate_distance(p1, p2)
        if distance > length1:
            return True
    return False


def lic_8_check(data_points, a_pts, b_pts, radius1):
    """Function for checking requirement LIC 8. Returns True
    if There exists at least one set of three data points separated by exactly A PTS and B PTS
    consecutive intervening points, respectively, that cannot be contained within or on a circle of
    radius RADIUS1. The condition is not met when NUMPOINTS < 5
    """
    if len(data_points) < 5 or a_pts < 1 or b_pts < 1 or (a_pts + b_pts > len(data_points) -3): 
        return False
    
    for i in range(len(data_points) - a_pts - b_pts - 2):
        p1 = data_points[i]
        p2 = data_points[i + a_pts + 1]
        p3 = data_points[i + a_pts + b_pts + 2]
        
        dist1 = sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) 
        dist2 = sqrt((p3[0] - p1[0])**2 + (p3[1] - p1[1])**2) 
        dist3 = sqrt((p3[0] - p2[0])**2 + (p3[1] - p2[1])**2)
        
        if max(dist1, dist2, dist3) > 2*radius1:
            return True
        
        # area of the triangle formed by the three points
        semi_perimeter = (dist1 + dist2 + dist3) / 2
        area = sqrt(semi_perimeter * (semi_perimeter - dist1) * (semi_perimeter - dist2) * (semi_perimeter - dist3))

        # colinearity check
        if area == 0:
            if max(dist1, dist2, dist3) <= 2 * radius1:
                continue
            else:
                return True

        circum_radius = (dist1 * dist2 * dist3) / (4 * area)
        if circum_radius > radius1:
            return True
        
    return False


def lic_9_check(data_points, c_pts, d_pts, epsilon):
    """Function for checking requirement LIC 9. Returns True
    if there exits 3 points, separated by C PTs and
    D PTS respectively, that form an angle that fulfills
    |angle - PI| > Epsilon"""
    if len(data_points) < 3 + c_pts + d_pts:
        return False
    for index in range(len(data_points) - c_pts - d_pts - 2):
        p1, p2, p3 = (data_points[index],
                      data_points[index + c_pts + 1],
                      data_points[index + c_pts + d_pts + 2])
        angle = calculate_angle(p1, p2, p3)
        if angle is None:
            continue
        if abs(angle - pi) > epsilon:
            return True
    return False


def lic_10_check(data_points, numpoints, e_pts, f_pts, area1):
    """There exists at least one set of three data points separated by exactly E PTS and F PTS consecutive intervening
    points, respectively, that are the vertices of a triangle with area greater
    than AREA1. The condition is not met when NUMPOINTS < 5.
    1 ≤ E PTS, 1 ≤ F PTS
    E PTS+F PTS ≤ NUMPOINTS−3
    """

    # Check for the appropriate numpoints values
    # Numpoints must be 5 or larger (because of minimal distances between the points),
    # and E PTS + F PTS ≤ NUMPOINTS − 3
    if numpoints < 5 or e_pts + f_pts > numpoints - 3:
        return False

    # Check for appropriate e_pts and f_pts values,
    # where e_pts, f_pts >= 1
    if e_pts < 1 or f_pts < 1:
        return False

    # Try to find a matching triangle of area larger than AREA1
    for index in range(numpoints - e_pts - f_pts - 2):
        p1 = data_points[index]
        p2 = data_points[index + e_pts + 1]
        p3 = data_points[index + e_pts + f_pts + 2]

        # Using following formula: 1/2 |x_1(y_2 - y_3) + x_2(y_3 - y_1) + x_3(y_1 - y_2)|
        area_triangle = calculate_triangle_area(p1, p2, p3)

        if area_triangle > area1:
            # Found a match
            return True

    # No match found
    return False


def lic_11_check(data_points, numpoints, g_pts):
    """There exists at least one set of two data points, (X[i],Y[i]) and (X[j],Y[j]), separated by
    exactly G PTS consecutive intervening points, such that X[j] - X[i] < 0. (where i < j ) The
    condition is not met when NUMPOINTS < 3.
    1 ≤ G PTS ≤ NUMPOINTS−2
    """

    # Check for appropriate values for numpoints and g_pts
    if numpoints < 3 or g_pts < 1 or g_pts > numpoints - 2:
        return False

    # Try to two points such that X[j] - X[i] < 0
    for index in range(numpoints - g_pts - 1):
        (x_1, _) = data_points[index]                   # Represents X[i]
        (x_2, _) = data_points[index + g_pts + 1]       # Represents X[j]

        if x_2 - x_1 < 0:
            # Found a match
            return True

    # No match found
    return False


def lic_12_check(data_points, numpoints, k_pts, length1, length2):
    """There exists at least one set of two data points, separated by exactly K PTS consecutive
    intervening points, which are a distance greater than the length, LENGTH1, apart. In addition,
    there exists at least one set of two data points (which can be the same or different from
    the two data points just mentioned), separated by exactly K PTS consecutive intervening
    points, that are a distance less than the length, LENGTH2, apart. Both parts must be true
    for the LIC to be true. The condition is not met when NUMPOINTS < 3.
    0 ≤ LENGTH2
    """

    # Check for appropriate values for numpoints and g_pts
    if numpoints < 3 or k_pts < 1 or k_pts > numpoints - 2:
        return False

    # Check for lengths to be 0 or larger
    if length1 < 0 or length2 < 0:
        return False

    larger_than_length1 = False
    smaller_than_length2 = False

    # Try to find distances to satisfy that at least a distance > length1, and a distance is < length2
    for index in range(numpoints - k_pts - 1):
        p1 = data_points[index]
        p2 = data_points[index + k_pts + 1]

        dist = calculate_distance(p1, p2)

        if not larger_than_length1 and dist > length1:
            larger_than_length1 = True

        if not smaller_than_length2 and dist < length2:
            smaller_than_length2 = True

        if larger_than_length1 and smaller_than_length2:
            # Found a match
            return True

    # No match found
    return False


def lic_13_check(data_points, radius1, radius2, a_pts, b_pts):
    """Function for LIC 13.

    Condition A: There exists at least
    one set of three data points, separated by exactly a_pts and
    b_pts consecutive points, respectively, that cannot be contained
    by a circle of radius radius1.

    Condition B: There exists at least one set of three data points
    separated by exactly a_pts and b_pts intervening points, respectively,
    that can be contained by a circle of radius radius2. """
    if len(data_points) < a_pts + b_pts + 3 or len(data_points) < 5:
        return False
    condition_a = False
    condition_b = False
    for index in range(len(data_points) - a_pts - b_pts - 2):
        p1, p2, p3 = (data_points[index],
                      data_points[index + a_pts + 1],
                      data_points[index + a_pts + b_pts + 2])
        distances = [calculate_distance(p1, p2), calculate_distance(p1, p3), calculate_distance(p2, p3)]
        max_distance = max(distances)
        if max_distance > 2 * radius1:
            condition_a = True
        if max_distance <= 2 * radius2:
            max_index = distances.index(max_distance)
            if max_index == 0:
                center = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
                if calculate_distance(center, p3) <= 2 * radius2:
                    condition_b = True
            elif max_index == 1:
                center = ((p1[0] + p3[0]) / 2, (p1[1] + p3[1]) / 2)
                if calculate_distance(center, p2) <= 2 * radius2:
                    condition_b = True
            else:
                center = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
                if calculate_distance(center, p1) <= 2 * radius2:
                    condition_b = True
        circumcenter = calculate_circumcenter(p1, p2, p3)
        if circumcenter is None:
            continue
        circumradius = calculate_distance(circumcenter, p1)
        if circumradius > radius1:
            condition_a = True
        if circumradius < radius2:
            condition_b = True
        if condition_a and condition_b:
            return True
    return False


def lic_14_check(
    data_points: list,
    e_pts: int,
    f_pts: int,
    area1: float,
    area2: float,
) -> bool:
    """
    LIC 14:
    Check if both apply:
    1. Three points, separated by E PTS and F PTS, form a triangle with area > AREA1.
    2. Three points (same or different), separated by E PTS and F PTS, form a triangle with area < AREA2.
    """
    num_points = len(data_points)

    if num_points < 5 or area2 < 0:
        return False

    condition_a_met = False
    condition_b_met = False

    for i in range(num_points):
        # calculate indices for the three points
        j = i + e_pts + 1
        k = j + f_pts + 1

        # within bounds
        if k >= num_points:
            continue

        p1 = data_points[i]
        p2 = data_points[j]
        p3 = data_points[k]

        area = calculate_triangle_area(p1, p2, p3)

        if not condition_a_met and area > area1:
            condition_a_met = True

        if not condition_b_met and area < area2:
            condition_b_met = True

        if condition_a_met and condition_b_met:
            return True

    return condition_a_met and condition_b_met
