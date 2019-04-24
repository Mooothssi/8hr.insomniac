
class Point():
    """
        A Cartesian point in a window
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, another):
        return Point(self.x + another.x, self.y + another.y)

    def __sub__(self, another):
        return Point(self.x - another.x, self.y - another.y)

    def __str__(self):
        return f"({self.x}, {self.y})"