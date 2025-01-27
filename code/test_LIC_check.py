import pytest
from LIC_check import *
from math import pi


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
def test_lic0_check(data_points, length1, expected):
    assert lic_0_check(data_points, length1) == expected


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
def test_lic2_check(data_points, epsilon, expected):
    assert lic_2_check(data_points, epsilon) == expected


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
def test_lic3_check(data_points, area1, expected):
    assert lic_3_check(data_points, area1) == expected


@pytest.mark.parametrize(
    "data_points, e_pts, f_pts, area1, numpoints, expected",
    [
        # TODO: Fix mismatch of len(data_points) and Numpoints
        # TODO: data_points should be points, to me coherent to the instructions
        # TODO: AREA1 should be equal or larger to 0
        # Test no data_points
        (
            [],
            1,
            1,
            40,
            0,
            False
        ),

        # Test NUMPOINTS < 5
        (
            [(0, 0), (1, 0), (10, 0), (1, 1)],
            1,
            1,
            40,
            4,
            False

        ),

        # Test E_PTS < 1
        (
            [(0, 0), (1, 0), (10, 0), (1, 1), (0, 10)],
            0,
            1,
            40,
            5,
            False
        ),

        # Test F_PTS < 1
        (
            [(0, 0), (1, 0), (10, 0), (1, 1), (0, 10)],
            1,
            0,
            40,
            5,
            False
        ),

        # E PTS+F PTS > NUMPOINTS−3
        (
            [(0, 0), (1, 0), (10, 0), (1, 1), (0, 10)],
            1,
            2,
            40,
            5,
            False
        ),

        # Test with all points the same
        (
            [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
            1,
            1,
            50,
            5,
            False
        ),

        # Test with all on the same line
        (
            [(0, 0), (1, 1), (2, 2), (3, 3), (4, 5)],
            1,
            1,
            1,
            5,
            False
        ),

        # Test no points larger than AREA1, area of [P0, P2, P4] (=50) < AREA1 (=60)
        (
                [(0, 0), (1, 0), (10, 0), (1, 1), (0, 10)],
                1,
                1,
                60,
                5,
                False
        ),

        # Test Area of [P0, P2, P4] (=25) == AREA1 (=50)
        (
            [(0, 0), (1, 0), (10, 0), (1, 1), (0, 10)],
            1,
            1,
            50,
            5,
            False
        ),

        # Test Area of [P0, P2, P4] (=25) > AREA1 (=40)
        (
            [(0, 0), (1, 0), (10, 0), (1, 1), (0, 10)],
            1,
            1,
            40,
            5,
            True
        ),

        # Test with 6 elements, [P0, P2, P4] are offset to [P1, P3, P5], doesn't start with the element in sequence
        (
            [(0, 1), (0, 0), (1, 0), (10, 0), (1, 1), (0, 10)],
            1,
            1,
            40,
            6,
            True
        ),

        # Test with 7 elements, doesn't end with the element in sequence
        (
            [(0, 1), (0, 0), (1, 0), (10, 0), (1, 1), (0, 10), (2, 2)],
            1,
            1,
            40,
            7,
            True
        ),

        # Test with more than minimal offset e_pts
        (
            [(0, 1), (0, 0), (1, 0), (1, 1), (10, 0), (2, 2), (0, 10), (3, 3)],
            2,
            1,
            40,
            8,
            True
        ),

        # Test with more than minimal offset f_pts
        (
            [(0, 1), (0, 0), (1, 0), (10, 0), (1, 1), (2, 2), (0, 10), (3, 3)],
            1,
            2,
            40,
            8,
            True
        ),

        # Test with more than minimal offset both e_pts and f_pts
        (
            [(0, 1), (0, 0), (1, 0), (1, 1), (10, 0), (2, 2), (3, 3), (0, 10), (4, 4)],
            2,
            2,
            40,
            9,
            True
        ),

        # Test with more point combinations being larger than the area
        (
            [(0, 1), (0, 0), (1, 0), (1, 1), (10, 0), (2, 2), (3, 3), (0, 10), (4, 4)],
            2,
            2,
            0.1,
            9,
            True
        ),
    ]
)
def test_lic10_check(data_points, e_pts, f_pts, area1, numpoints, expected):
    assert lic_10_check(data_points, e_pts, f_pts, area1, numpoints) == expected


@pytest.mark.parametrize(
    "p1, p2, p3, expected",
    [
        ((0, 0), (0, 0), (0, 0), 0),
        ((1, 1), (1, 1), (1, 1), 0),
        ((0, 1), (1, 0), (-1, 0), 1),
        ((0, 10), (-1, -7), (3, -11), 36),
        ((-10, 5), (-10, -5), (10, 0), 100),
        ((-9, -3234), (-7, -8), (60903, 8), 98247814),
    ],
)
def test_calculate_triangle_area(p1, p2, p3, expected):
    assert calculate_triangle_area(p1, p2, p3) == expected


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
def test_lic_14_check(data_points, e_pts, f_pts, area1, area2, expected):
    assert lic_14_check(data_points, e_pts, f_pts, area1, area2) == expected
