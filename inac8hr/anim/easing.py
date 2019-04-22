import math


class EasingBase:
    """
        Based on Penner's easing functions
    """
    limit = (0, 1)

    def __init__(self, start=0, end=1, duration=1):
        self.start = start
        self.end = end
        self.duration = duration

    @classmethod
    def func(cls, t):
        pass

    def ease(self, alpha):
        t = self.limit[0] * (1 - alpha) + self.limit[1] * alpha
        t /= self.duration
        r = self.func(t)
        return self.end * r + self.start * (1 - r)


"""
    Quadratic (x^2) easing functions
"""


class QuadEaseIn(EasingBase):
    def func(self, t):
        return t * t
