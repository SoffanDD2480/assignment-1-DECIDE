import pytest
from decide import Decide


def test_numpoints_initial_assignment():
    """Test that NUMPOINTS can be set initially."""
    decide = Decide()
    decide.NUMPOINTS = 5
    assert decide.NUMPOINTS == 5, "NUMPOINTS should be set to 5"


def test_numpoints_immutable_after_set():
    """Test that NUMPOINTS cannot be changed after initial assignment."""
    decide = Decide()
    decide.NUMPOINTS = 5

    with pytest.raises(
        AttributeError,
        match="NUMPOINTS is immutable and cannot be changed after it is set",
    ):
        decide.NUMPOINTS = 10


def test_numpoints_invalid_type():
    """Test that NUMPOINTS raises an error if assigned a non-integer."""
    decide = Decide()

    with pytest.raises(
        ValueError, match="NUMPOINTS must be an integer between 0 and 100"
    ):
        decide.NUMPOINTS = "five"  # Invalid type


def test_numpoints_invalid_range():
    """Test that NUMPOINTS raises an error if assigned an out-of-range value."""
    decide = Decide()

    with pytest.raises(
        ValueError, match="NUMPOINTS must be an integer between 0 and 100"
    ):
        decide.NUMPOINTS = -1  # Negative value

    with pytest.raises(
        ValueError, match="NUMPOINTS must be an integer between 0 and 100"
    ):
        decide.NUMPOINTS = 101  # Greater than 100


def test_points_initial_assignment():
    """Test that POINTS can be set initially."""
    decide = Decide()
    points = [(0, 0), (1, 1), (2, 2)]
    decide.POINTS = points
    assert decide.POINTS == points, "POINTS should match the assigned list"


def test_points_invalid_type():
    """Test that POINTS raises an error if assigned a non-list or invalid tuples."""
    decide = Decide()

    with pytest.raises(
        ValueError,
        match="POINTS must be a list of tuples, each containing exactly 2 elements",
    ):
        decide.POINTS = "invalid_points"  # Not a list

    with pytest.raises(
        ValueError,
        match="POINTS must be a list of tuples, each containing exactly 2 elements",
    ):
        decide.POINTS = [(0, 0), (1,)]  # Tuple with fewer than 2 elements

    with pytest.raises(
        ValueError,
        match="POINTS must be a list of tuples, each containing exactly 2 elements",
    ):
        decide.POINTS = [(0, 0), "not_a_tuple"]  # List contains a non-tuple element


def test_points_invalid_coordinates():
    """Test that POINTS raises an error if elements are not numeric."""
    decide = Decide()

    with pytest.raises(
        ValueError, match="POINTS must contain only numeric coordinates"
    ):
        decide.POINTS = [(0, 0), (1, "not_numeric")]  # Second coordinate is not numeric


def test_points_length_mismatch_with_numpoints():
    """Test that POINTS raises an error if its length doesn't match NUMPOINTS."""
    decide = Decide()
    decide.NUMPOINTS = 3

    with pytest.raises(
        ValueError, match="POINTS must have the same length as NUMPOINTS"
    ):
        decide.POINTS = [(0, 0), (1, 1)]  # Length is less than NUMPOINTS


def test_points_length_out_of_bounds():
    """Test that POINTS raises an error if the length is out of bounds."""
    decide = Decide()

    with pytest.raises(
        ValueError, match="POINTS must contain between 0 and 100 points"
    ):
        decide.POINTS = [(0, 0)] * 101  # More than 100 points
