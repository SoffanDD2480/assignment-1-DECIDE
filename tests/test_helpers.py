import pytest
from math import sqrt
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from decide.helpers import (
    calculate_distance,
    calculate_triangle_area,
    calculate_circumcenter,
)


class TestAllHelpers:
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
    def test_calculate_triangle_area(self, p1, p2, p3, expected):
        assert calculate_triangle_area(p1, p2, p3) == expected

    @pytest.mark.parametrize(
        "p1, p2, expected",
        [
            ((0, 0), (0, 0), 0),
            ((1, 1), (1, 1), 0),
            ((-1, -1), (2, 3), 5),
            ((0, 0), (-6, -8), 10),
            ((1, 0), (0, 1), sqrt(2)),
            ((-2468, -3702), (2468, 0), 6170),
            ((-10, -10), (-6, -7), 5),
        ],
    )
    def test_calculate_distance(self, p1, p2, expected):
        assert calculate_distance(p1, p2) == expected

    @pytest.mark.parametrize(
        "p1, p2, p3, expected",
        [
            ((0, 0), (0, 0), (0, 0), None),  # coinciding points, no circumcircle
            ((0, 0), (1, 0), (0, 0), None),  # 2 points coincide, no circumcircle
            ((0, 0), (1, 1), (2, 2), None),  # colinear points, no circumcircle
            (
                (0, 0),
                (2, 0),
                (1, 3**0.5),
                (1.00000000000000, 0.577350269189626),
            ),  # Equilateral triangle
            ((0, 0), (0, 1), (1, 1), (0.5, 0.5)),  # Right triangle
            ((-1, -1), (0.2, -0.2), (1, 1), (-2.4, 2.4)),  # Almost colinear
        ],
    )
    def test_calculate_circumcenter(self, p1, p2, p3, expected):
        assert calculate_circumcenter(p1, p2, p3) == expected
