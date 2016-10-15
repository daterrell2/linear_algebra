from math import sqrt, acos, pi
from decimal import Decimal, getcontext, InvalidOperation

getcontext().prec = 30


class Vector:

    def __init__(self, *coordinates):
        if not coordinates:
            raise ValueError('The coordinates must be nonempty')
        try:
            self.coordinates = tuple(Decimal(c) for c in coordinates)
        except InvalidOperation:
            raise ValueError('The coordinates must be numeric')

        self.dimension = len(coordinates)

    @property
    def magnitude(self):
        return Decimal(sqrt(sum(c**2 for c in self.coordinates)))

    def normalize(self):
        try:
            return self.__mul__(Decimal('1.0')/self.magnitude)
        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    def is_zero(self, tolerance=1e-10):
        return self.magnitude < tolerance

    def round(self, precision):
        return Vector(*[round(c, precision) for c in self.coordinates])

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __add__(self, v):
        return Vector(*tuple(c1 + c2 for c1, c2 in zip(self.coordinates, v.coordinates)))

    def __sub__(self, v):
        return Vector(*tuple(c1 - c2 for c1, c2 in zip(self.coordinates, v.coordinates)))

    def __mul__(self, s):
        return Vector(*tuple(c * Decimal(s) for c in self.coordinates))

    def __rmul__(self, s):
        return self.__mul__(s)

    def projection(self, b):
        if b.is_zero():
            raise Exception('No parallel component to the zero vector')
        u = b.normalize()
        return u * dot(self, u)

    def rejection(self, b):
        if b.is_zero():
            raise Exception('No orthogonal component to the zero vector')
        return self - self.projection(b)


def dot(v1, v2):
    return sum(c1*c2 for c1, c2 in zip(v1.coordinates, v2.coordinates))


def angle(v1, v2, degrees=False):
    try:
        u1 = v1.normalize()
        u2 = v2.normalize()
        angle = acos(round(Vector.dot(u1, u2), 3))
        if degrees:
            return angle * (180/pi)
        return angle

    except Exception as e:
        raise e


def is_orthogonal(v1, v2, tolerance=1e-10):
    return abs(Vector.dot(v1, v2)) < tolerance


def is_parallel(v1, v2):
    return v1.is_zero() or v2.is_zero() or Vector.angle(v1, v2) in (0, pi)


def cross_product(v1, v2):
    if not v1.dimension == v2.dimension == 3:
        raise Exception('Can only calucate the cross product of 3-dimensional vectors')
    x1, y1, z1 = v1.coordinates
    x2, y2, z2 = v2.coordinates
    return Vector(y1*z2 - y2*z1,
                  -(x1*z2 - x2*z1),
                  (x1*y2 - x2*y1))
