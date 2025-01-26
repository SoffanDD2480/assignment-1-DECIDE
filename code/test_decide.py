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


def test_calculate_PUM():
    """
    Test the calculate_PUM method with different LCM and CMV configurations.
    """
    decide = Decide()

    # Example setup
    decide._CMV = [
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
        True,
    ]

    # Test LCM with all "ANDD"
    decide._LCM = [["ANDD"] * 15 for _ in range(15)]
    decide.calculate_PUM()
    for i in range(15):
        for j in range(15):
            assert decide._PUM[i][j] == (decide._CMV[i] and decide._CMV[j]), (
                f"PUM[{i}][{j}] should be CMV[{i}] AND CMV[{j}]"
            )

    # Test LCM with all "ORR"
    decide._LCM = [["ORR"] * 15 for _ in range(15)]
    decide.calculate_PUM()
    for i in range(15):
        for j in range(15):
            assert decide._PUM[i][j] == (decide._CMV[i] or decide._CMV[j]), (
                f"PUM[{i}][{j}] should be CMV[{i}] OR CMV[{j}]"
            )

    # Test LCM with all "NOTUSED"
    decide._LCM = [["NOTUSED"] * 15 for _ in range(15)]
    decide.calculate_PUM()
    for i in range(15):
        for j in range(15):
            assert decide._PUM[i][j] is True, (
                f"PUM[{i}][{j}] should be True for NOTUSED"
            )

    # Test Mixed LCM
    decide._LCM = [
        ["ANDD", "ORR", "NOTUSED", "ANDD", "ORR"] + ["NOTUSED"] * 10,
        ["ORR", "ANDD", "ORR", "NOTUSED", "ANDD"] + ["NOTUSED"] * 10,
    ] + [["NOTUSED"] * 15 for _ in range(13)]
    decide.calculate_PUM()
    assert decide._PUM[0][1] == (decide._CMV[0] or decide._CMV[1]), (
        "PUM[0][1] should be CMV[0] OR CMV[1]"
    )
    assert decide._PUM[0][2] is True, "PUM[0][2] should be True for NOTUSED"
    assert decide._PUM[1][4] == (decide._CMV[1] and decide._CMV[4]), (
        "PUM[1][4] should be CMV[1] AND CMV[4]"
    )


def test_calculate_FUV():
    """Test the calculate_FUV method with different configurations of PUV and PUM."""
    decide = Decide()

    # Test when PUV values are False
    decide._PUV = [False] * 15
    decide._PUM = [[False] * 15 for _ in range(15)]
    decide.calculate_FUV()
    assert all(decide._FUV), "All FUV values should be True when PUV is all False"

    # Test when all PUV values are True, and all rows in PUM are True
    decide._PUV = [True] * 15
    decide._PUM = [[True] * 15 for _ in range(15)]
    decide.calculate_FUV()
    assert all(decide._FUV), (
        "All FUV values should be True when PUV is all True and PUM rows are all True"
    )

    # Test when all PUV values are True, and some rows in PUM contain False
    decide._PUV = [True] * 15
    decide._PUM = [[True] * 15 for _ in range(15)]
    decide._PUM[2][3] = False
    decide.calculate_FUV()
    assert not decide._FUV[2], "FUV[2] should be False because PUM[2] contains a False"
    for i in range(15):
        if i != 2:
            assert decide._FUV[i], (
                f"FUV[{i}] should be True because row {i} in PUM is all True"
            )

    # Test Mixed PUV values
    decide._PUV = [True, False, True, False, True] + [False] * 10
    decide._PUM = [[True] * 15 for _ in range(15)]
    decide.calculate_FUV()
    for i in range(15):
        if decide._PUV[i]:
            assert decide._FUV[i], (
                f"FUV[{i}] should be True because PUV[{i}] is True and PUM[{i}] is all True"
            )
        else:
            assert decide._FUV[i], f"FUV[{i}] should be True because PUV[{i}] is False"
