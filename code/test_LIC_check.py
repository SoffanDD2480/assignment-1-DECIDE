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
