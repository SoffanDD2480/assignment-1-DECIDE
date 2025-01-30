import pytest
from math import pi
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from decide import Decide


class TestAllLicChecks:
    @pytest.mark.parametrize(
        "data_points, length1, expected",
        [
            ([(0, 0), (3, 4)], 5, False),  # Distance = 5
            ([(0, 0), (4, 5)], 5, True),  # Distance ≈ 6.403
            (
                [(0, 0), (1, 1), (2, 2), (3, 3)],
                2,
                False,
            ),  # All distances < 2
            (
                [(0, 0), (1, 1), (4, 5), (3, 3)],
                4,
                True,
            ),  # Distance between (1,1) and (4,5) ≈ 5 > 4
        ],
    )
    def test_lic_0_check(self, data_points, length1, expected):
        decide = Decide()
        decide.POINTS = data_points
        decide.LENGTH1 = length1
        assert decide.LIC.lic_0_check() == expected

    @pytest.mark.parametrize(
        "data_points, radius1, expected",
        [
            (
                [(0, 0), (1, 1)],
                5.0,
                False,
            ),  # Only two points
            (
                [
                    (0, 0),
                    (10, 0),
                    (5, 5),
                ],
                4.0,
                True,
            ),
            (
                [
                    (0, 0),
                    (3.9, 0),
                    (1.95, 3.376),
                ],
                2.0,
                True,
            ),
            (
                [
                    (0, 0),
                    (3, 0),
                    (1.5, 2.598),
                ],
                2.0,
                False,
            ),
            (
                [(0, 0), (1, 1), (2, 2)],
                2.0,
                False,
            ),  # colinear
            (
                [(1, 1), (1, 1), (1, 1)],
                0.0,
                False,
            ),  # identical points
        ],
    )
    def test_lic_1_check(self, data_points, radius1, expected):
        decide = Decide()
        decide.POINTS = data_points
        decide.RADIUS1 = radius1
        assert decide.LIC.lic_1_check() == expected

    @pytest.mark.parametrize(
        "data_points, epsilon, expected",
        [
            ([(0, 0), (1, 1)], pi / 4, False),  # Less than three data points
            (
                [(1, 0), (0, 0), (-1, 0)],
                pi / 2,
                False,
            ),  # Angle at p2 90 degrees = pi - pi/2
            (
                [(1, 0), (0, 0), (2, -1)],
                pi / 2,
                True,
            ),  # Angle at p2 ~26 degrees < pi + pi/2
            (
                [(0, 0), (1, 0), (2, 0)],
                pi / 4,
                False,
            ),  # All angles = pi
            (
                [(0, 0), (0, 0), (1, 1), (1, 1), (2, 2)],
                pi / 4,
                False,
            ),  # All valid angles are pi
            (
                [(0, 0), (1, 0), (1, 1)],
                0,
                True,
            ),  # Any angle != pi satisfies with epsilon=0
            (
                [(0, 0), (1, 0), (1, 1), (1, 1)],
                0,
                True,
            ),  # Non-colinear triplet satisfies with epsilon=0
        ],
    )
    def test_lic_2_check(self, data_points, epsilon, expected):
        decide = Decide()
        decide.POINTS = data_points
        decide.EPSILON = epsilon
        assert decide.LIC.lic_2_check() == expected

    @pytest.mark.parametrize(
        "data_points, area1, expected",
        [
            ([(0, 0), (1, 1)], 1, False),  # Less than three data points
            (
                [(0, 0), (1, 1), (2, 2)],
                0.5,
                False,
            ),  # area = 0
            (
                [(0, 0), (1, 0), (0, 1)],
                1,
                False,
            ),  # Area = 0.5 <= 1
            (
                [(0, 0), (2, 0), (0, 2)],
                1,
                True,
            ),  # Area = 2.0 > 1
            (
                [
                    (0, 0),
                    (1, 0),
                    (0, 1),
                    (1, 1),
                    (2, 1),
                    (1, 2),
                ],
                1,
                False,
            ),  # All triangle areas = 0.5 <= 1
            (
                [
                    (0, 0),
                    (1, 0),
                    (0, 1),
                    (0, 0),
                    (3, 0),
                    (0, 3),
                ],
                1,
                True,
            ),  # One triangle area = 4.5 > 1
            (
                [(0, 0), (2, 0), (0, 2)],
                2.0,
                False,
            ),  # Area = 2.0 == 2.0
            (
                [(0, 0), (1, 0), (0, 1)],
                0,
                True,
            ),  # Area = 0.5 > 0
            (
                [
                    (0, 0),
                    (1, 0),
                    (1, 1),
                    (2, 0),
                    (2, 2),
                    (3, 1),
                ],
                -1,
                True,
            ),  # area1 negative, always True
            (
                [
                    (0, 0),
                    (1000000, 0),
                    (0, 1000000),
                ],
                1,
                True,
            ),  # Very large area
            (
                [(0, 0), (1, 1), (2, 2)],
                0,
                False,
            ),  # Colinear, area = 0, not > 0
        ],
    )
    def test_lic_3_check(self, data_points, area1, expected):
        decide = Decide()
        decide.POINTS = data_points
        decide.AREA1 = area1
        assert decide.LIC.lic_3_check() == expected

    @pytest.mark.parametrize(
        "data_points, q_pts, quads, expected",
        [
            # Less data points than q_pts
            (
                [(0, 0), (1, 0)],
                3,
                1,
                False,
            ),
            # Test with all points in the same quadrant but quadrants covered <= quads
            (
                [(0, 0), (1, 1), (2, 2), (3, 3)],
                4,
                1,
                False,
            ),
            # Test with all points in different quadrants
            (
                [(0, 0), (-1, 1), (2, -2), (-3, -3)],
                4,
                1,
                True,
            ),
            # Test with points distributed in two quadrants and quadrants covered > quads
            (
                [(1, 1), (-1, 1), (2, 2)],
                3,
                1,
                True,
            ),
            # Test with three point distribuition in three quadrants and quadrants covered > quads
            (
                [(1, 1), (-1, 1), (2, -2)],
                3,
                1,
                True,
            ),
            # Test with all the points in the origin
            (
                [(0, 0), (0, 0), (0, 0), (0, 0)],
                4,
                1,
                False,
            ),
        ],
    )
    def test_lic_4_check(self, data_points, q_pts, quads, expected):
        decide = Decide()
        decide.POINTS = data_points
        decide.Q_PTS = q_pts
        decide.QUADS = quads
        assert decide.LIC.lic_4_check() == expected

    @pytest.mark.parametrize(
        "data_points, expected",
        [
            # Test with two consecutive points such that x[j] - x[i] >= 0
            (
                [(0, 0), (1, 0)],
                False,
            ),
            # Test with two consecutive points such that x[j] - x[i] < 0
            (
                [(1, 0), (0, 0)],
                True,
            ),
            # Test with three consecutive points such that x[j] - x[i] >= 0
            (
                [(0, 0), (1, 0), (2, 0)],
                False,
            ),
            # Test with three consecutive points with at least one couple such that x[j] - x[i] < 0
            (
                [(0, 0), (2, 0), (1, 0)],
                True,
            ),
            # Test with three consecutive points such that x[j] - x[i] < 0
            (
                [(3, 0), (2, 0), (1, 0)],
                True,
            ),
        ],
    )
    def test_lic_5_check(self, data_points, expected):
        decide = Decide()
        decide.POINTS = data_points
        assert decide.LIC.lic_5_check() == expected

    @pytest.mark.parametrize(
        "data_points, dist, n_pts, expected",
        [
            # Test with less points than n_pts
            (
                [(0, 0), (1, 0)],
                1,
                3,
                False,
            ),
            # Test with three points such that distance bewteen them is more than dist
            (
                [(0, 0), (1, 2), (2, 0)],
                1,
                3,
                True,
            ),
            # Test with three points such that distance bewteen them is less than dist
            (
                [(0, 0), (1, 1), (2, 0)],
                2,
                3,
                False,
            ),
            # Test with two coicident points and one point at a distance more than dist
            (
                [(0, 0), (0, 0), (2, 0)],
                1,
                3,
                False,
            ),
            # Test with two coicident points and one point at a distance less than dist
            (
                [(0, 0), (0, 0), (1, 0)],
                2,
                3,
                False,
            ),
            # Test with three points at the same distance
            (
                [(0, 0), (1, 0), (2, 0)],
                1,
                3,
                False,
            ),
            # Test with multiple sets of points, one satisfies the condition
            (
                [(0, 0), (1, 1), (2, 0), (3, 3)],
                1,
                3,
                True,
            ),
        ],
    )
    def test_lic_6_check(self, data_points, dist, n_pts, expected):
        decide = Decide()
        decide.POINTS = data_points
        decide.DIST = dist
        decide.N_PTS = n_pts
        assert decide.LIC.lic_6_check() == expected

    @pytest.mark.parametrize(
        "data_points, k_pts, length1, expected",
        [
            # Test with less than 3 points
            (
                [(0, 0), (1, 1)],
                1,
                1,
                False,
            ),
            # Test with k_pts > numpoints
            (
                [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
                10,
                1,
                False,
            ),
            # Test with two points of length = 2 apart
            (
                [(0, 0), (-1, -1), (2, 0)],
                1,
                1,
                True,
            ),
            # Test with all points in the origin
            (
                [(0, 0), (0, 0), (0, 0)],
                1,
                1,
                False,
            ),
            # Test with k_pts = 3, second loop is valid
            (
                [(0, 0), (0, 0), (-1, -1), (4, 4), (1, 0), (1, 1)],
                3,
                1,
                True,
            ),
            # Test with k_pts = 0, second loop is valid
            (
                [(0, 0), (0, 0), (-1, -1), (4, 4), (1, 0), (1, 1)],
                0,
                1,
                False,
            ),
        ],
    )
    def test_lic_7_check(self, data_points, k_pts, length1, expected):
        decide = Decide()
        decide.POINTS = data_points
        decide.K_PTS = k_pts
        decide.LENGTH1 = length1
        assert decide.LIC.lic_7_check() == expected

    @pytest.mark.parametrize(
        "data_points, a_pts, b_pts, radius1, expected",
        [
            # Test with less then 5 points
            (
                [(0, 0), (1, 1), (2, 2), (3, 3)],
                1,
                1,
                1,
                False,
            ),
            # Test with a_pts < 1
            (
                [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
                0,
                1,
                1,
                False,
            ),
            # Test with b_pts < 1
            (
                [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
                1,
                0,
                1,
                False,
            ),
            # Test with a_pts + b_pts > numpoints - 3
            (
                [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
                2,
                2,
                1,
                False,
            ),
            # Test with three points in a circle with radius1
            (
                [(0, 0), (1, 0), (2, 0), (1, 1), (0, 2)],
                1,
                1,
                3,
                False,
            ),
            # Test with three points NOT in a circle with radius1
            (
                [(0, 0), (1, 0), (2, 0), (1, 1), (0, 6)],
                1,
                1,
                1,
                True,
            ),
            # Test with collinear points
            (
                [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
                1,
                1,
                1,
                True,
            ),
            # Test with all points in the origin
            (
                [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                1,
                1,
                1,
                False,
            ),
        ],
    )
    def test_lic_8_check(self, data_points, a_pts, b_pts, radius1, expected):
        decide = Decide()
        decide.POINTS = data_points
        decide.A_PTS = a_pts
        decide.B_PTS = b_pts
        decide.RADIUS1 = radius1
        assert decide.LIC.lic_8_check() == expected

    @pytest.mark.parametrize(
        "data_points, c_pts, d_pts, epsilon, expected",
        [
            # Test with less then 5 points
            (
                [(0, 0), (1, 1), (2, 2), (3, 3)],
                1,
                1,
                1,
                False,
            ),
            # Test with c_pts < 1
            (
                [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
                0,
                1,
                1,
                False,
            ),
            # Test with d_pts < 1
            (
                [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
                1,
                0,
                1,
                False,
            ),
            # Test with c_pts + d_pts + 3 > numpoints
            (
                [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
                2,
                2,
                1,
                False,
            ),
            # Test with colinear points, epsilon = 0.01
            (
                [(0, 0), (1, -1), (1, 1), (-1, 1), (2, 2)],
                1,
                1,
                0.01,
                False,
            ),
            # Test with points in origin
            (
                [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                1,
                1,
                1,
                False,
            ),
            # Test with 90 deg angle, smaller epsilon
            (
                [(0, 0), (1, -1), (1, 0), (-1, 1), (1, 1)],
                1,
                1,
                1,
                True,
            ),
            # Test with 90 deg angle, larger epsilon
            (
                [(0, 0), (1, -1), (1, 0), (-1, 1), (1, 1)],
                1,
                1,
                2,
                False,
            ),
            # Test with larger 90 deg and 45 deg angle
            (
                [
                    (0, 0),
                    (1, 0),
                    (10, 10),
                    (-10, -10),
                    (1, 0),
                    (0, 0),
                    (-10, 10),
                    (10, -10),
                    (1, 1),
                    (1, 1),
                ],
                3,
                3,
                2,
                True,
            ),
        ],
    )
    def test_lic_9_check(self, data_points, c_pts, d_pts, epsilon, expected):
        decide = Decide()
        decide.POINTS = data_points
        decide.C_PTS = c_pts
        decide.D_PTS = d_pts
        decide.EPSILON = epsilon
        assert decide.LIC.lic_9_check() == expected

    @pytest.mark.parametrize(
        "data_points, numpoints, e_pts, f_pts, area1, expected",
        [
            # Test NUMPOINTS < 5
            ([(0, 0), (1, 0), (10, 0), (1, 1)], 4, 1, 1, 40, False),
            # Test E_PTS < 1
            ([(0, 0), (1, 0), (10, 0), (1, 1), (0, 10)], 5, 0, 1, 40, False),
            # Test F_PTS < 1
            ([(0, 0), (1, 0), (10, 0), (1, 1), (0, 10)], 5, 1, 0, 40, False),
            # E PTS+F PTS > NUMPOINTS−3
            ([(0, 0), (1, 0), (10, 0), (1, 1), (0, 10)], 5, 1, 2, 40, False),
            # Test with all points the same
            ([(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)], 5, 1, 1, 50, False),
            # Test with all on the same line
            ([(0, 0), (1, 1), (2, 2), (3, 3), (4, 5)], 5, 1, 1, 1, False),
            # Test no points larger than AREA1, area of [P0, P2, P4] (=50) < AREA1 (=60)
            ([(0, 0), (1, 0), (10, 0), (1, 1), (0, 10)], 5, 1, 1, 60, False),
            # Test Area of [P0, P2, P4] (=25) == AREA1 (=50)
            ([(0, 0), (1, 0), (10, 0), (1, 1), (0, 10)], 5, 1, 1, 50, False),
            # Test Area of [P0, P2, P4] (=25) > AREA1 (=40)
            ([(0, 0), (1, 0), (10, 0), (1, 1), (0, 10)], 5, 1, 1, 40, True),
            # Test with 6 elements, [P0, P2, P4] are offset to [P1, P3, P5], doesn't start with the element in sequence
            ([(0, 1), (0, 0), (1, 0), (10, 0), (1, 1), (0, 10)], 6, 1, 1, 40, True),
            # Test with 7 elements, doesn't end with the element in sequence
            (
                [(0, 1), (0, 0), (1, 0), (10, 0), (1, 1), (0, 10), (2, 2)],
                7,
                1,
                1,
                40,
                True,
            ),
            # Test with more than minimal offset e_pts
            (
                [(0, 1), (0, 0), (1, 0), (1, 1), (10, 0), (2, 2), (0, 10), (3, 3)],
                8,
                2,
                1,
                40,
                True,
            ),
            # Test with more than minimal offset f_pts
            (
                [(0, 1), (0, 0), (1, 0), (10, 0), (1, 1), (2, 2), (0, 10), (3, 3)],
                8,
                1,
                2,
                40,
                True,
            ),
            # Test with more than minimal offset both e_pts and f_pts
            (
                [
                    (0, 1),
                    (0, 0),
                    (1, 0),
                    (1, 1),
                    (10, 0),
                    (2, 2),
                    (3, 3),
                    (0, 10),
                    (4, 4),
                ],
                9,
                2,
                2,
                40,
                True,
            ),
            # Test with more point combinations being larger than the area
            (
                [
                    (0, 1),
                    (0, 0),
                    (1, 0),
                    (1, 1),
                    (10, 0),
                    (2, 2),
                    (3, 3),
                    (0, 10),
                    (4, 4),
                ],
                9,
                2,
                2,
                0.1,
                True,
            ),
        ],
    )
    def test_lic_10_check(self, data_points, numpoints, e_pts, f_pts, area1, expected):
        decide = Decide()
        decide.NUMPOINTS = numpoints
        decide.POINTS = data_points
        decide.E_PTS = e_pts
        decide.F_PTS = f_pts
        decide.AREA1 = area1
        assert decide.LIC.lic_10_check() == expected

    @pytest.mark.parametrize(
        "data_points, numpoints, g_pts, expected",
        [
            # Test NUMPOINTS < 3
            ([(1, 0), (0, 0)], 2, 1, False),
            # Test G_PTS < 1
            ([(1, 0), (0, 0), (0, 1)], 3, 0, False),
            # Test G_PTS > NUMPOINTS−2
            ([(1, 0), (0, 0), (0, 1)], 3, 2, False),
            # Test with all points the same
            ([(0, 0), (0, 0), (0, 0)], 3, 1, False),
            # Test x_1 < x_2
            ([(0, 1), (0, 0), (1, 0)], 3, 1, False),
            # Test x_1 == x_2
            ([(0, 1), (0, 0), (0, 2)], 3, 1, False),
            # Test x_1 > x_2
            ([(1, 0), (0, 0), (0, 1)], 3, 1, True),
            # Test with extra element in the beginning
            ([(-2, 2), (1, 0), (0, 0), (0, 1)], 4, 1, True),
            # Test with extra element in at the end
            ([(-2, 2), (1, 0), (0, 0), (0, 1), (3, 3)], 5, 1, True),
            # Test with non-minimal offset
            ([(-2, 2), (1, 0), (0, 0), (3, 3), (0, 1), (4, 4)], 6, 2, True),
            # Test with multiple right answers
            ([(-2, 2), (1, 0), (5, 5), (3, 3), (1, 1), (4, 4), (2, 2)], 7, 2, True),
        ],
    )
    def test_lic_11_check(self, data_points, numpoints, g_pts, expected):
        decide = Decide()
        decide.NUMPOINTS = numpoints
        decide.POINTS = data_points
        decide.G_PTS = g_pts
        assert decide.LIC.lic_11_check() == expected

    @pytest.mark.parametrize(
        "data_points, numpoints, k_pts, length1, length2, expected",
        [
            # Test NUMPOINTS < 3
            ([(0, 0), (2, 2)], 2, 1, 0, 1, False),
            # Test K_PTS < 1 (assuming it should be that K_PTS >= 1, as with LIC 12)
            ([(0, 0), (2, 2), (1, 0)], 3, 0, 0, 2, False),
            # Test K_PTS > NUMPOINTS−2 (assuming, same as with LIC 11)
            ([(0, 0), (2, 2), (1, 0)], 3, 2, 0, 2, False),
            # Test with all points the same
            ([(0, 0), (0, 0), (0, 0)], 3, 1, 1, 2, False),
            # Test with length1 < 0
            ([(0, 0), (2, 2), (1, 0)], 3, 1, -1, 2, False),
            # Test with length2 < 0
            ([(0, 0), (2, 2), (1, 0)], 3, 1, 0, -1, False),
            # Test with same dist, length1 (=0) < calc dist (=1), but calc dist (=1) > length2 (=0)
            ([(0, 0), (2, 2), (1, 0)], 3, 1, 0, 0, False),
            # Test with same dist, length2 (=0) > calc dist (=1), but calc dist (=1) < length1 (=2)
            ([(0, 0), (2, 2), (1, 0)], 3, 1, 2, 2, False),
            # Test with same dist, length1 (=0) < calc dist (=1) < length2 (=2)
            ([(0, 0), (2, 2), (1, 0)], 3, 1, 0, 2, True),
            # Test with 2 dist, dist1 (=1) < length2 (=5), length1 (=3) < dist2 (=4) < length2 (=5)
            ([(1, 0), (0, 0), (1, 1), (4, 0)], 4, 1, 3, 5, True),
            # Test with 2 dist, dist1 (=1) < length2 (=5), length1 (=3) < dist2 (=10)
            ([(1, 0), (0, 0), (1, 1), (10, 0)], 4, 1, 3, 5, True),
            # Test with 2 dist, dist1 (=1) < length2 (=2), length1 (=3) < dist2 (=4)
            ([(1, 0), (0, 0), (1, 1), (4, 0)], 4, 1, 3, 2, True),
            # Test with 2 dist, dist1 (=4) > length1 (=3), length2 (=2) > dist2 (=1)
            ([(0, 0), (1, 0), (4, 0), (1, 1)], 4, 1, 3, 2, True),
            # Test with extra distance
            ([(1, 0), (0, 0), (1, 1), (4, 0), (0, 1)], 5, 1, 3, 5, True),
            # Test non-minimal offset
            ([(1, 0), (0, 0), (1, 1), (10, 0), (0, 1)], 5, 2, 3, 5, True),
        ],
    )
    def test_lic_12_check(
        self, data_points, numpoints, k_pts, length1, length2, expected
    ):
        decide = Decide()
        decide.NUMPOINTS = numpoints
        decide.POINTS = data_points
        decide.K_PTS = k_pts
        decide.LENGTH1 = length1
        decide.LENGTH2 = length2
        assert decide.LIC.lic_12_check() == expected

    @pytest.mark.parametrize(
        "data_points, a_pts, b_pts, radius1, radius2, expected",
        [
            # Test with a_pts < 1
            (
                [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                0,
                1,
                1,
                1,
                False,
            ),
            # Test with b_pts < 1
            (
                [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                1,
                0,
                1,
                1,
                False,
            ),
            # Test with a_pts and b_pts < 1
            (
                [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                0,
                1,
                1,
                1,
                False,
            ),
            # Test with a_pts + b_pts + 3 > numpoints
            (
                [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                2,
                2,
                1,
                1,
                False,
            ),
            # Both conditions met
            (
                [(0, 0), (0, 0), (5, 0), (1, 0), (4, 4), (0.1, 0.5)],
                1,
                1,
                2.5,
                1,
                True,
            ),
            # Only condition A met
            (
                [(0, 0), (0, 0), (3, 0), (1, 0), (1, 0), (0.5, 0)],
                1,
                1,
                1,
                0.2,
                False,
            ),
            # Only condition B met
            (
                [(0, 0), (0, 0), (3, 0), (1, 0), (1, 0), (0.5, 0)],
                1,
                1,
                3,
                1,
                False,
            ),
        ],
    )
    def test_lic_13_check(self, data_points, a_pts, b_pts, radius1, radius2, expected):
        decide = Decide()
        decide.POINTS = data_points
        decide.A_PTS = a_pts
        decide.B_PTS = b_pts
        decide.RADIUS1 = radius1
        decide.RADIUS2 = radius2
        assert decide.LIC.lic_13_check() == expected

    @pytest.mark.parametrize(
        "data_points, e_pts, f_pts, area1, area2, expected",
        [
            (
                [(0, 0), (1, 1), (2, 2), (3, 3)],
                1,
                1,
                1.0,
                2.0,
                False,
            ),  # insufficient data
            (
                [
                    (0, 0),
                    (4, 0),
                    (4, 3),
                    (0, 3),
                    (1, 1),
                    (2, 2),
                ],
                2,
                1,
                2.0,
                4.0,
                True,
            ),  # both conditions
            (
                [
                    (0, 0),
                    (3, 0),
                    (3, 4),
                    (0, 4),
                    (1, 1),
                    (4, 1),
                ],
                1,
                1,
                2.0,
                5.0,
                True,
            ),  # both conditions
            (
                [
                    (0, 0),
                    (5, 0),
                    (5, 5),
                    (0, 5),
                    (1, 1),
                ],
                1,
                1,
                10.0,
                5.0,
                False,
            ),  # only condition A
            (
                [
                    (0, 0),
                    (1, 0),
                    (1, 1),
                    (2, 1),
                    (2, 2),
                ],
                1,
                1,
                1.0,
                1.0,
                False,
            ),  # only condition B
            (
                [
                    (0, 0),
                    (1, 0),
                    (1, 1),
                    (2, 1),
                    (2, 2),
                ],
                1,
                1,
                1.0,
                -1.0,
                False,
            ),  # invalid AREA2
        ],
    )
    def test_lic_14_check(self, data_points, e_pts, f_pts, area1, area2, expected):
        decide = Decide()
        decide.POINTS = data_points
        decide.E_PTS = e_pts
        decide.F_PTS = f_pts
        decide.AREA1 = area1
        decide.AREA2 = area2
        assert decide.LIC.lic_14_check() == expected
