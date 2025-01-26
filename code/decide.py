import math


class Decide:
    def __init__(self):
        self._NUMPOINTS = None
        self._POINTS = []  # List of planar data points
        self._CMV = [False] * 15  # Conditions Met Vector
        self._LCM = [["NOTUSED"] * 15 for _ in range(15)]  # Logical Connector Matrix
        self._PUM = [
            [True for _ in range(15)] for _ in range(15)
        ]  # Preliminary Unlocking Matrix
        self.PUV = [False] * 15  # Preliminary Unlocking Vector
        self._FUV = [False] * 15  # Final Unlocking Vector
        self._LAUNCH = "NO"

        # Parameters
        self.LENGTH1 = 0
        self.RADIUS1 = 0
        self.EPSILON = 0
        self.AREA1 = 0
        self.LENGTH2 = 0
        self.RADIUS2 = 0
        self.AREA2 = 0
        self.Q_PTS = 0
        self.QUADS = 0
        self.DIST = 0
        self.N_PTS = 0
        self.K_PTS = 0
        self.A_PTS = 0
        self.B_PTS = 0
        self.C_PTS = 0
        self.D_PTS = 0
        self.E_PTS = 0
        self.F_PTS = 0
        self.G_PTS = 0

    @property
    def NUMPOINTS(self):
        return self._NUMPOINTS

    @NUMPOINTS.setter
    def NUMPOINTS(self, value):
        if self._NUMPOINTS is not None:
            raise AttributeError(
                "NUMPOINTS is immutable and cannot be changed after it is set"
            )
        if not isinstance(value, int) or not (2 <= value <= 100):
            raise ValueError("NUMPOINTS must be an integer between 0 and 100")
        self._NUMPOINTS = value

    @property
    def POINTS(self):
        return self._POINTS

    @POINTS.setter
    def POINTS(self, value):
        if not isinstance(value, list) or not all(
            isinstance(point, tuple) and len(point) == 2 for point in value
        ):
            raise ValueError(
                "POINTS must be a list of tuples, each containing exactly 2 elements"
            )
        if not all(
            isinstance(coord, (int, float)) for point in value for coord in point
        ):
            raise ValueError(
                "POINTS must contain only numeric coordinates (int or float)"
            )
        if self.NUMPOINTS is not None and len(value) != self.NUMPOINTS:
            raise ValueError("POINTS must have the same length as NUMPOINTS")
        if not (2 <= len(value) <= 100):
            raise ValueError("POINTS must contain between 0 and 100 points")

        self._POINTS = value
        if self.NUMPOINTS is None:  # Set NUMPOINTS if it hasn't been set
            self.NUMPOINTS = len(value)


if __name__ == "__main__":
    decide = Decide()
    # Example inputs
    decide.NUMPOINTS = 5
    decide.POINTS = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
    decide.LENGTH1 = 1.5
    decide.LCM = [["ANDD"] * 15 for _ in range(15)]
    decide.PUV = [True] * 15

    print(f"Launch Decision: {decide.decide()}")
