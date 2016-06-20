class Vector:

    def __init__(self, coordinates):
        if not coordinates:
            raise ValueError('The coordinates must be nonempty')
        
        try:
            self.coordinates = tuple(coordinates)
        except TypeError:
            raise TypeError('The coordinates must be an iterable')
        
        self.dimension = len(coordinates)

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __add__(self, v):
        return Vector(tuple(c1 + c2 for c1, c2 in zip(self.coordinates, v.coordinates)))

    def __sub__(self, v):
        return Vector(tuple(c1 - c2 for c1, c2 in zip(self.coordinates, v.coordinates)))

    def __mul__(self, s):
        return Vector(tuple(c * s for c in self.coordinates))
