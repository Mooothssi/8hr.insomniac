import numpy as np
import arcade


class Point():
    """
        A Cartesian coordinate in a window
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
    
    def __eq__(self, another):
        return self.x == another.x and self.y == another.y

    def to_list(self):
        return [self.x, self.y]


class Margin():
    """
        Defines outer space of a control
        (Typically used with an anchor)
    """
    __slots__ = ['left', 'right', 'bottom', 'top']

    def __init__(self, left=0, bottom=0, top=0, right=0):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top

    def __str__(self):
        return f"Margin(top: {self.top}, left: {self.left}, bottom: {self.bottom}, right: {self.right})"


class Padding(Margin):
    """
        Defines inner space of a control around its content.
    """
    __slots__ = ['left', 'right', 'bottom', 'top']

    def __str__(self):
        return f"Padding(top: {self.top}, left: {self.left}, bottom: {self.bottom}, right: {self.right})"


class Region():
    """
        A polygonal boundary of a control
        which is useful for cursor hit-checking
    """
    def __init__(self, bottom_left: Point, bottom_right: Point,
                 top_left: Point, top_right: Point):
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right
        self.top_left = top_left
        self.top_right = top_right
        self.vertex_loop = None

    def point_overlap(self, p: Point):
        if self.bottom_left <= p.x <= self.bottom_right \
           and self.top_left <= p.y <= self.top_right:
            return True
        else:
            return False


class RectangularRegion():
    """
        A rectangular boundary of a control
        which is useful for cursor hit-checking
    """
    VERTEX_POINT_COUNT = 4

    def __init__(self, *vertices):
        self.vertex_loop = []
        if len(vertices) > self.VERTEX_POINT_COUNT:
            raise Exception("Maximum vertex point count exceeded")
        for vertex in vertices:
            self.vertex_loop.append(vertex)

    def __str__(self):
        return f"RectangularRegion [{self.vertex_loop[0]},"\
        f" {self.vertex_loop[1]}, {self.vertex_loop[2]},"\
        f" {self.vertex_loop[3]}]"

    def is_point_inside(self, p: Point):
        p1 = self.vertex_loop[3]
        p2 = self.vertex_loop[2]
        p3 = self.vertex_loop[0]
        p1p2 = np.array((p2 - p1).to_list())
        p1p = np.array((p - p1).to_list())
        p1p3 = np.array((p3 - p1).to_list())
        return 0 <= np.dot(p1p2, p1p) <= np.dot(p1p2, p1p2) and 0 <= np.dot(p1p3, p1p) <= np.dot(p1p3, p1p3)

    def draw(self):
        arcade.draw_lrtb_rectangle_outline(left=self.vertex_loop[0].x, right=self.vertex_loop[1].x,
                                            bottom=self.vertex_loop[0].y, top=self.vertex_loop[2].y, color=arcade.color.RED)
