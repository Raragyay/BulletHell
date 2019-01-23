# coding=utf-8
"""
Holds PVector class for specialized math.
"""
from math import ceil, floor, sqrt, cos, sin, atan, atan2, trunc


class PVector:
    """
    Main class for all velocities and positions. Used for nodes, pixel positions, and velocities.
    """

    def __init__(self, x=0.0, y=0.0):
        """
        Top left is (0,0)
        :param x: Horizontal Location or Velocity
        :param y: Vertical Location or Velocity
        """
        self.x = x
        self.y = y

    def __str__(self):
        return "PVector (x,y): {0:.10f},{1:.10f}".format(self.x, self.y)

    def __repr__(self):
        return f'{self.x} {self.y}'

    def __add__(self, other: 'PVector') -> 'PVector':
        return PVector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'PVector') -> 'PVector':
        return PVector(self.x - other.x, self.y - other.y)

    def __eq__(self, other: 'PVector') -> bool:
        return other and self.x == other.x and self.y == other.y

    def __ne__(self, other: 'PVector') -> bool:
        return self.x != other.x and self.y != other.y

    def __neg__(self) -> 'PVector':
        return self * -1

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __abs__(self) -> 'PVector':
        return PVector(abs(self.x), abs(self.y))

    def __int__(self):
        return PVector(int(self.x), int(self.y))

    def __mul__(self, scalar: float) -> 'PVector':
        return PVector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> 'PVector':
        return PVector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> 'PVector':
        return PVector(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar: float) -> 'PVector':
        return PVector(self.x // scalar, self.y // scalar)

    def __mod__(self, scalar: float) -> 'PVector':
        return PVector(self.x % scalar, self.y % scalar)

    def __ceil__(self) -> 'PVector':
        return PVector(ceil(self.x), ceil(self.y))

    def __floor__(self) -> 'PVector':
        return PVector(floor(self.x), floor(self.y))

    def __round__(self) -> 'PVector':
        if self.x < 0:
            new_x = floor(self.x)
        else:
            new_x = ceil(self.x)
        if self.y < 0:
            new_y = floor(self.y)
        else:
            new_y = ceil(self.y)
        return PVector(new_x, new_y)

    def __lt__(self, other: 'PVector') -> bool:
        return self.x < other.x and self.y < other.y

    def __le__(self, other: 'PVector') -> bool:
        return self.x <= other.x and self.y <= other.y

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, key: int):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        else:
            raise IndexError(f"Index out of bounds for PVector: {key}")

    def copy(self):
        return PVector(self.x, self.y)

    def dist_from(self, other: 'PVector') -> float:
        """
        Calculate euclidean distance between two points
        :param other: PVector
        :return: float value
        """
        manhattan = abs(self - other)
        euclidean = sqrt(manhattan.x ** 2 + manhattan.y ** 2)
        return euclidean

    @staticmethod
    def from_tuple(tup: tuple) -> 'PVector':
        """
        Converts tuple to PVector
        :param tup: Two element tuple
        :return: PVector
        """
        return PVector(tup[0], tup[1])

    def flip_x(self, in_place=False):
        if in_place:
            self.x *= -1
        else:
            return PVector(self.x * -1, self.y)

    def flip_y(self, in_place=False):
        if in_place:
            self.y *= -1
        else:
            return PVector(self.x, self.y * -1)

    def project(self, angle, radius) -> 'PVector':
        """

            :param pos: If moving sprite, this is sprite position. Otherwise would be (0,0) with creation of PVector
            :param angle: Angle in radians in standard position
            :param radius: "speed" of sprite
            :return: PVector(x,y)
            """
        return self + PVector(cos(angle), -sin(angle)) * radius  # -sin because y increases as it goes down

    def angle_to(self, target: 'PVector') -> float:
        """
        Returns in radians the angle to the object
        :param target:
        :return:
        """
        manhattan = (target - self).flip_y()
        return atan2(manhattan.y, manhattan.x)

    def trunc(self) -> 'PVector':
        return PVector(trunc(self.x), trunc(self.y))
