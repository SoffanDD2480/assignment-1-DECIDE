from math import sqrt, pi

from .helpers import (
    calculate_distance,
    calculate_triangle_area,
    calculate_circumcenter,
    calculate_angle,
)


class LIC:
    """Class encapsulating all Launch Interceptor Conditions (LICs)."""

    def __init__(self, decide_instance):
        self.decide = decide_instance

    def lic_0_check(self):
        """Function for checking requirement LIC 0. Returns True
        if there exists 2 consecutive points with a distance
        larger than length1, False otherwise."""
        if len(self.decide.POINTS) < 2:
            return False
        for index in range(len(self.decide.POINTS) - 1):
            p1 = self.decide.POINTS[index]
            p2 = self.decide.POINTS[index + 1]
            dist = calculate_distance(p1, p2)
            if dist > self.decide.LENGTH1:
                return True
        return False

    def lic_1_check(self):
        """Function for checking requirement LIC 1. Returns True
        if there exists 3 consecutive points that cannot fit within
        a circle of radius radius1, False otherwise.
        """
        if len(self.decide.POINTS) < 3:
            return False
        for index in range(len(self.decide.POINTS) - 2):
            p1, p2, p3 = (
                self.decide.POINTS[index],
                self.decide.POINTS[index + 1],
                self.decide.POINTS[index + 2],
            )
            dist1 = calculate_distance(p1, p2) > 2 * self.decide.RADIUS1
            dist2 = calculate_distance(p1, p3) > 2 * self.decide.RADIUS1
            dist3 = calculate_distance(p2, p3) > 2 * self.decide.RADIUS1
            if dist1 or dist2 or dist3:
                return True
            circumcenter = calculate_circumcenter(p1, p2, p3)
            if circumcenter is None:
                continue
            if calculate_distance(circumcenter, p1) > self.decide.RADIUS1:
                return True
        return False

    def lic_2_check(self):
        """function that checks the LIC 2. Returns True if there exists at least one set
        of three consecutive data points which form an angle such that the angle is:
        less than pi - epsilon
        greater than pi + epsilon.
        """

        for i in range(len(self.decide.POINTS) - 2):
            p1, p2, p3 = (
                self.decide.POINTS[i],
                self.decide.POINTS[i + 1],
                self.decide.POINTS[i + 2],
            )
            angle = calculate_angle(p1, p2, p3)

            if angle == None:
                continue

            if angle < (pi - self.decide.EPSILON) or angle > (pi + self.decide.EPSILON):
                return True
        return False

    def lic_3_check(self):
        """function that checks the LIC 3. Returns True if there exists at least one set
        of three consecutive data points which form a triangle with area greater than area1.
        """
        for i in range(len(self.decide.POINTS) - 2):
            p1, p2, p3 = (
                self.decide.POINTS[i],
                self.decide.POINTS[i + 1],
                self.decide.POINTS[i + 2],
            )
            area = calculate_triangle_area(p1, p2, p3)

            """if the area is 0, the points are aligned"""
            if area == 0:
                continue

            if area > self.decide.AREA1:
                return True
        return False

    def lic_4_check(self):
        """function that checks the LIC 4. Returns True if there exists at least one set
        of q_pts consecutive data points that lie in more than quads quadrants.
        """

        if self.decide.Q_PTS <= 0 or len(self.decide.POINTS) < self.decide.Q_PTS:
            return False

        for i in range(len(self.decide.POINTS) - self.decide.Q_PTS + 1):
            quadrants = set()
            for j in range(i, i + self.decide.Q_PTS):
                x, y = self.decide.POINTS[j]
                if x >= 0 and y >= 0:
                    quadrants.add(1)
                elif x < 0 and y > 0:
                    quadrants.add(2)
                elif x < 0 and y < 0:
                    quadrants.add(3)
                elif x > 0 and y < 0:
                    quadrants.add(4)

            if len(quadrants) > self.decide.QUADS:
                return True

        return False

    def lic_5_check(self):
        """function that check the LIC 5. Returns True if there exists at least one set of two consecutive data points,
        (x[i],y[i]) and (x[j],y[j]), such that x[j] - x[i] < 0.
        """
        for i in range(len(self.decide.POINTS) - 1):
            x_i = self.decide.POINTS[i]
            x_j = self.decide.POINTS[i + 1]

            if x_j[0] - x_i[0] < 0:
                return True

        return False

    def lic_6_check(self):
        """function that check the LIC 6. Returns True if there exists at least one set of n_pts consecutive data points
        such that at least one of the point lies a distance greater than dist from the line joining the first and last of these n_pts points.
        If the first and last points of these N PTS are identical, then the calculated distance
        to compare with DIST will be the distance from the coincident point to all other points of
        the N PTS consecutive points. The condition is not met when NUMPOINTS < 3.
        """

        if (
            (len(self.decide.POINTS) < 3)
            or (self.decide.N_PTS > len(self.decide.POINTS))
            or (self.decide.DIST < 0)
        ):
            return False

        for i in range(len(self.decide.POINTS) - self.decide.N_PTS + 1):
            p1 = self.decide.POINTS[i]
            p2 = self.decide.POINTS[i + self.decide.N_PTS - 1]

            if p1 == p2:
                for j in range(i + 1, i + self.decide.N_PTS - 1):
                    p = self.decide.POINTS[j]
                    distance_calculated = calculate_distance(p1, p)
                    if distance_calculated > self.decide.DIST:
                        return True

            else:
                for j in range(i + 1, i + self.decide.N_PTS - 1):
                    p = self.decide.POINTS[j]
                    distance_calculated = abs(
                        (p2[0] - p1[0]) * (p1[1] - p[1])
                        - (p1[0] - p[0]) * (p2[1] - p1[1])
                    ) / sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
                    if distance_calculated > self.decide.DIST:
                        return True

        return False

    def lic_7_check(self):
        """Function for checking requirement LIC 7. Returns True
        if there exists 2 points, K_PTS consecutive interveining
        points apart with distance LENGTH1 between them, False
        otherwise.
        """
        if (
            len(self.decide.POINTS) < 3
            or len(self.decide.POINTS) - 2 < self.decide.K_PTS
            or self.decide.K_PTS < 1
        ):
            return False
        for index in range(len(self.decide.POINTS) - self.decide.K_PTS - 1):
            p1 = self.decide.POINTS[index]
            p2 = self.decide.POINTS[index + self.decide.K_PTS + 1]
            distance = calculate_distance(p1, p2)
            if distance > self.decide.LENGTH1:
                return True
        return False

    def lic_8_check(self):
        """Function for checking requirement LIC 8. Returns True
        if There exists at least one set of three data points separated by exactly A PTS and B PTS
        consecutive intervening points, respectively, that cannot be contained within or on a circle of
        radius RADIUS1. The condition is not met when NUMPOINTS < 5
        """
        if (
            len(self.decide.POINTS) < 5
            or self.decide.A_PTS < 1
            or self.decide.B_PTS < 1
            or (self.decide.A_PTS + self.decide.B_PTS > len(self.decide.POINTS) - 3)
        ):
            return False

        for i in range(
            len(self.decide.POINTS) - self.decide.A_PTS - self.decide.B_PTS - 2
        ):
            p1 = self.decide.POINTS[i]
            p2 = self.decide.POINTS[i + self.decide.A_PTS + 1]
            p3 = self.decide.POINTS[i + self.decide.A_PTS + self.decide.B_PTS + 2]

            dist1 = calculate_distance(p1, p2)
            dist2 = calculate_distance(p3, p1)
            dist3 = calculate_distance(p3, p2)

            if max(dist1, dist2, dist3) > 2 * self.decide.RADIUS1:
                return True

            semi_perimeter = (dist1 + dist2 + dist3) / 2
            area = sqrt(
                semi_perimeter
                * (semi_perimeter - dist1)
                * (semi_perimeter - dist2)
                * (semi_perimeter - dist3)
            )

            if area == 0:
                continue

            circum_radius = (dist1 * dist2 * dist3) / (4 * area)
            if circum_radius > self.decide.RADIUS1:
                return True

        return False

    def lic_9_check(self):
        """Function for checking requirement LIC 9. Returns True
        if there exits 3 points, separated by C PTs and
        D PTS respectively, that form an angle that fulfills
        |angle - PI| > Epsilon"""
        if (
            len(self.decide.POINTS) < 3 + self.decide.C_PTS + self.decide.D_PTS
            or self.decide.C_PTS < 1
            or self.decide.D_PTS < 1
        ):
            return False
        for index in range(
            len(self.decide.POINTS) - self.decide.C_PTS - self.decide.D_PTS - 2
        ):
            p1, p2, p3 = (
                self.decide.POINTS[index],
                self.decide.POINTS[index + self.decide.C_PTS + 1],
                self.decide.POINTS[index + self.decide.C_PTS + self.decide.D_PTS + 2],
            )
            angle = calculate_angle(p1, p2, p3)
            if angle is None:
                continue
            if abs(angle - pi) > self.decide.EPSILON:
                return True
        return False

    def lic_10_check(self):
        """There exists at least one set of three data points separated by exactly E PTS and F PTS consecutive intervening
        points, respectively, that are the vertices of a triangle with area greater
        than AREA1. The condition is not met when NUMPOINTS < 5.
        1 ≤ E PTS, 1 ≤ F PTS
        E PTS+F PTS ≤ NUMPOINTS−3
        """

        # Check for the appropriate numpoints values
        # Numpoints must be 5 or larger (because of minimal distances between the points),
        # and E PTS + F PTS ≤ NUMPOINTS − 3
        if (
            self.decide.NUMPOINTS < 5
            or self.decide.E_PTS + self.decide.F_PTS > self.decide.NUMPOINTS - 3
        ):
            return False

        # Check for appropriate e_pts and f_pts values,
        # where e_pts, f_pts >= 1
        if self.decide.E_PTS < 1 or self.decide.F_PTS < 1:
            return False

        # Try to find a matching triangle of area larger than AREA1
        for index in range(
            self.decide.NUMPOINTS - self.decide.E_PTS - self.decide.F_PTS - 2
        ):
            p1 = self.decide.POINTS[index]
            p2 = self.decide.POINTS[index + self.decide.E_PTS + 1]
            p3 = self.decide.POINTS[index + self.decide.E_PTS + self.decide.F_PTS + 2]

            # Using following formula: 1/2 |x_1(y_2 - y_3) + x_2(y_3 - y_1) + x_3(y_1 - y_2)|
            area_triangle = calculate_triangle_area(p1, p2, p3)

            if area_triangle > self.decide.AREA1:
                # Found a match
                return True

        # No match found
        return False

    def lic_11_check(self):
        """There exists at least one set of two data points, (X[i],Y[i]) and (X[j],Y[j]), separated by
        exactly G PTS consecutive intervening points, such that X[j] - X[i] < 0. (where i < j ) The
        condition is not met when NUMPOINTS < 3.
        1 ≤ G PTS ≤ NUMPOINTS−2
        """

        # Check for appropriate values for numpoints and g_pts
        if (
            self.decide.NUMPOINTS < 3
            or self.decide.G_PTS < 1
            or self.decide.G_PTS > self.decide.NUMPOINTS - 2
        ):
            return False

        # Try to two points such that X[j] - X[i] < 0
        for index in range(self.decide.NUMPOINTS - self.decide.G_PTS - 1):
            (x_1, _) = self.decide.POINTS[index]  # Represents X[i]
            (x_2, _) = self.decide.POINTS[
                index + self.decide.G_PTS + 1
            ]  # Represents X[j]

            if x_2 - x_1 < 0:
                # Found a match
                return True

        # No match found
        return False

    def lic_12_check(self):
        """There exists at least one set of two data points, separated by exactly K PTS consecutive
        intervening points, which are a distance greater than the length, LENGTH1, apart. In addition,
        there exists at least one set of two data points (which can be the same or different from
        the two data points just mentioned), separated by exactly K PTS consecutive intervening
        points, that are a distance less than the length, LENGTH2, apart. Both parts must be true
        for the LIC to be true. The condition is not met when NUMPOINTS < 3.
        0 ≤ LENGTH2
        """

        # Check for appropriate values for numpoints and g_pts
        if (
            self.decide.NUMPOINTS < 3
            or self.decide.K_PTS < 1
            or self.decide.K_PTS > self.decide.NUMPOINTS - 2
        ):
            return False

        # Check for lengths to be 0 or larger
        if self.decide.LENGTH1 < 0 or self.decide.LENGTH2 < 0:
            return False

        larger_than_length1 = False
        smaller_than_length2 = False

        # Try to find distances to satisfy that at least a distance > length1, and a distance is < length2
        for index in range(self.decide.NUMPOINTS - self.decide.K_PTS - 1):
            p1 = self.decide.POINTS[index]
            p2 = self.decide.POINTS[index + self.decide.K_PTS + 1]

            dist = calculate_distance(p1, p2)

            if not larger_than_length1 and dist > self.decide.LENGTH1:
                larger_than_length1 = True

            if not smaller_than_length2 and dist < self.decide.LENGTH2:
                smaller_than_length2 = True

            if larger_than_length1 and smaller_than_length2:
                # Found a match
                return True

        # No match found
        return False

    def lic_13_check(self):
        """Function for LIC 13.

        Condition A: There exists at least
        one set of three data points, separated by exactly self.decide.A_PTS and
        b_pts consecutive points, respectively, that cannot be contained
        by a circle of radius radius1.

        Condition B: There exists at least one set of three data points
        separated by exactly a_pts and b_pts intervening points, respectively,
        that can be contained by a circle of radius radius2."""
        if (
            len(self.decide.POINTS) < self.decide.A_PTS + self.decide.B_PTS + 3
            or len(self.decide.POINTS) < 5
            or self.decide.A_PTS < 1
            or self.decide.B_PTS < 1
        ):
            return False
        condition_a = False
        condition_b = False
        for index in range(
            len(self.decide.POINTS) - self.decide.A_PTS - self.decide.B_PTS - 2
        ):
            p1, p2, p3 = (
                self.decide.POINTS[index],
                self.decide.POINTS[index + self.decide.A_PTS + 1],
                self.decide.POINTS[index + self.decide.A_PTS + self.decide.B_PTS + 2],
            )
            distances = [
                calculate_distance(p1, p2),
                calculate_distance(p1, p3),
                calculate_distance(p2, p3),
            ]
            max_distance = max(distances)
            if max_distance > 2 * self.decide.RADIUS1:
                condition_a = True
            if max_distance <= 2 * self.decide.RADIUS2:
                max_index = distances.index(max_distance)
                if max_index == 0:
                    center = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
                    if calculate_distance(center, p3) <= 2 * self.decide.RADIUS2:
                        condition_b = True
                elif max_index == 1:
                    center = ((p1[0] + p3[0]) / 2, (p1[1] + p3[1]) / 2)
                    if calculate_distance(center, p2) <= 2 * self.decide.RADIUS2:
                        condition_b = True
                else:
                    center = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
                    if calculate_distance(center, p1) <= 2 * self.decide.RADIUS2:
                        condition_b = True
            circumcenter = calculate_circumcenter(p1, p2, p3)
            if circumcenter is None:
                continue
            circumradius = calculate_distance(circumcenter, p1)
            if circumradius > self.decide.RADIUS1:
                condition_a = True
            if circumradius < self.decide.RADIUS2:
                condition_b = True
            if condition_a and condition_b:
                return True
        if condition_a and condition_b:
            return True
        return False

    def lic_14_check(self):
        """
        LIC 14:
        Check if both apply:
        1. Three points, separated by E PTS and F PTS, form a triangle with area > AREA1.
        2. Three points (same or different), separated by E PTS and F PTS, form a triangle with area < AREA2.
        """
        num_points = len(self.decide.POINTS)

        if num_points < 5 or self.decide.AREA2 < 0:
            return False

        condition_a_met = False
        condition_b_met = False

        for i in range(num_points):
            # calculate indices for the three points
            j = i + self.decide.E_PTS + 1
            k = j + self.decide.F_PTS + 1

            # within bounds
            if k >= num_points:
                continue

            p1 = self.decide.POINTS[i]
            p2 = self.decide.POINTS[j]
            p3 = self.decide.POINTS[k]

            area = calculate_triangle_area(p1, p2, p3)

            if not condition_a_met and area > self.decide.AREA1:
                condition_a_met = True

            if not condition_b_met and area < self.decide.AREA2:
                condition_b_met = True

            if condition_a_met and condition_b_met:
                return True

        return condition_a_met and condition_b_met
