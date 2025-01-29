import math
from LIC_check import *


def gen_input(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file]
    numpoints = int(lines[0])
    data_points = [tuple(map(float, line.split()))
                   for line in lines[1:numpoints + 1]]
    float_parameters = list(map(float, lines[numpoints + 1:numpoints + 9]))
    int_parameters = list(map(int, lines[numpoints + 9:numpoints + 20]))
    parameters = float_parameters + int_parameters
    lcm = [line.split() for line in lines[numpoints + 20:numpoints + 35]]
    puv = [line == 'true' for line in lines[numpoints+35:]]
    return numpoints, data_points, parameters, lcm, puv


class Decide:
    def __init__(self, numpoints, data_points, parameters, lcm, puv):
        self._NUMPOINTS = numpoints
        self._POINTS = data_points  # List of planar data points
        self._CMV = [False] * 15  # Conditions Met Vector
        self._LCM = lcm  # Logical Connector Matrix
        self._PUM = [
            [True for _ in range(15)] for _ in range(15)
        ]  # Preliminary Unlocking Matrix
        self._PUV = puv  # Preliminary Unlocking Vector
        self._FUV = [False] * 15  # Final Unlocking Vector
        self._LAUNCH = "NO"

        # Parameters
        self.LENGTH1 = parameters[0]
        self.RADIUS1 = parameters[1]
        self.EPSILON = parameters[2]
        self.AREA1 = parameters[3]
        self.LENGTH2 = parameters[4]
        self.RADIUS2 = parameters[5]
        self.AREA2 = parameters[6]
        self.DIST = parameters[7]
        self.QUADS = parameters[8]
        self.Q_PTS = parameters[9]
        self.N_PTS = parameters[10]
        self.K_PTS = parameters[11]
        self.A_PTS = parameters[12]
        self.B_PTS = parameters[13]
        self.C_PTS = parameters[14]
        self.D_PTS = parameters[15]
        self.E_PTS = parameters[16]
        self.F_PTS = parameters[17]
        self.G_PTS = parameters[18]

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

    def evaluate_lic_0(self):
        return lic_0_check(self._POINTS, self.LENGTH1)

    def evaluate_lic_1(self):
        return lic_1_check(self._POINTS, self.RADIUS1)

    def evaluate_lic_2(self):
        return lic_2_check(self._POINTS, self.EPSILON)

    def evaluate_lic_3(self):
        return lic_3_check(self._POINTS, self.AREA1)

    def evaluate_lic_4(self):
        return lic_4_check(self._POINTS, self.Q_PTS, self.QUADS)

    def evaluate_lic_5(self):
        return lic_5_check(self._POINTS)

    def evaluate_lic_6(self):
        return lic_6_check(self._POINTS, self.DIST, self.N_PTS)

    def evaluate_lic_7(self):
        return lic_7_check(self._POINTS, self.K_PTS, self.LENGTH1)

    def evaluate_lic_8(self):
        return lic_8_check(self._POINTS, self.A_PTS, self.B_PTS, self.RADIUS1)

    def evaluate_lic_9(self):
        return lic_9_check(self._POINTS, self.C_PTS, self.D_PTS, self.EPSILON)

    def evaluate_lic_10(self):
        return lic_10_check(self._POINTS, self.NUMPOINTS, self.E_PTS, self.F_PTS, self.AREA1)

    def evaluate_lic_11(self):
        return lic_11_check(self._POINTS, self.NUMPOINTS, self.G_PTS)

    def evaluate_lic_12(self):
        return lic_12_check(self._POINTS, self.NUMPOINTS, self.K_PTS, self.LENGTH1, self.LENGTH2)

    def evaluate_lic_13(self):
        return lic_13_check(self._POINTS, self.RADIUS1, self.RADIUS2, self.A_PTS, self.B_PTS)

    def evaluate_lic_14(self):
        return lic_14_check(self._POINTS, self.E_PTS, self.F_PTS, self.AREA1, self.AREA2)

    def calculate_CMV(self):
        """
        Compute the Conditions Met Vector (CMV).

        The CMV is a list of boolean values indicating whether each
        of the 15 conditions (LIC 0 to LIC 14) is met.
        """
        # Mapping of LIC indices to their corresponding evaluation methods
        LIC_methods = [
            # boilerplate code for LICs
            self.evaluate_lic_0,
            self.evaluate_lic_1,
            self.evaluate_lic_2,
            self.evaluate_lic_3,
            self.evaluate_lic_4,
            self.evaluate_lic_5,
            self.evaluate_lic_6,
            self.evaluate_lic_7,
            self.evaluate_lic_8,
            self.evaluate_lic_9,
            self.evaluate_lic_10,
            self.evaluate_lic_11,
            self.evaluate_lic_12,
            self.evaluate_lic_13,
            self.evaluate_lic_14,
        ]

        for index, LIC_method in enumerate(LIC_methods):
            condition_met = LIC_method()
            self._CMV[index] = condition_met

    def calculate_PUM(self):
        """
        Compute the Preliminary Unlocking Matrix (PUM).

        The PUM is a 15x15 matrix where each element PUM[i][j] is determined
        based on the Logical Connection Matrix (LCM) and the Conditions Met Vector (CMV).

        Logical Operations:
            - "ANDD": Logical AND between CMV[i] and CMV[j].
            - "ORR" : Logical OR between CMV[i] and CMV[j].
            - "NOTUSED": Always True, indicating no condition.
        """
        for i in range(15):
            for j in range(15):
                if self._LCM[i][j] == "ANDD":
                    self._PUM[i][j] = self._CMV[i] and self._CMV[j]
                elif self._LCM[i][j] == "ORR":
                    self._PUM[i][j] = self._CMV[i] or self._CMV[j]
                elif self._LCM[i][j] == "NOTUSED":
                    self._PUM[i][j] = True

    def calculate_FUV(self):
        """
        Compute the Final Unlocking Vector (FUV).

        The FUV is a list of boolean values indicating whether each of the 15 final
        conditions is met based on the Preliminary Unlocking Vector (PUV) and
        the Preliminary Unlocking Matrix (PUM).

        Logic:
            - If PUV[i] is False, FUV[i] is automatically set to True.
            - If PUV[i] is True, FUV[i] is set to True only if all values in the corresponding
              row of PUM are True.
        """
        for i in range(15):
            if not self._PUV[i]:  # If PUV[i] is False, automatically set FUV[i] to True
                self._FUV[i] = True
            else:  # If PUV[i] is True, check the corresponding row in PUM
                self._FUV[i] = all(self._PUM[i])

    def decide(self):
        """
        The main function to compute the final launch decision.
        This function evaluates CMV, PUM, and FUV and determines whether
        the launch is permitted.
        """
        self.calculate_CMV()
        self.calculate_PUM()
        self.calculate_FUV()

        # If all values in the FUV are True, launch is permitted
        self._LAUNCH = "YES" if all(self._FUV) else "NO"
        return self._LAUNCH


if __name__ == "__main__":
    numpoints, data_points, parameters, lcm, puv = gen_input("../test_cases/test_case_1")
    decide = Decide(numpoints, data_points, parameters, lcm, puv)
    print(decide.decide())
