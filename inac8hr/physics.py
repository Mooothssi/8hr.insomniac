import math


class BasePhysicsEntity():
    def __init__(self, points):
        self.x1 = points[0]
        self.y1 = points[1]

    @staticmethod
    def collides(self, another):
        pass


class CirclePhysicsEntity(BasePhysicsEntity):

    def __init__(self, points, radius):
        super().__init__(points)
        x1, y1 = self.x1, self.y1
        # x2 = points[1][0]
        # y2 = points[1][1]
        self.radius = radius  # math.sqrt(pow(x2-x1, 2) + pow(y2-y1, 2))
        # self.rx, self.ry = x2, y2

    def collides(self, another):
        return self.eval_dist(another) <= self.radius + another.radius

    def closest(self, another):
        return self.eval_dist(another) - self.radius - another.radius

    def closest_rad(self, another):
        return self.closest(another)

    def eval_dist(self, c2):
        x2, y2 = c2.x1, c2.y1
        return math.sqrt(pow(x2-self.x1, 2) + pow(y2-self.y1, 2))
