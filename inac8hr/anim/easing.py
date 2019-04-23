import math


class EasingBase:
    """
        Based on Penner's easing (gentle motion) functions
        Courtesy of Semitable (https://github.com/semitable/easing-functions)

        Args:
            start (int): The start position of the function
            end (int): The end position of the function (multiplier)
            duration (int): Time duration of easing
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
        return self.end * r + self.start * (1 - r)  # reduced from c*p(t) + b


"""
    Linear easing functions
    [p(x) = x]
"""


class LinearEase(EasingBase):
    def func(self, t):
        return t


"""
    Quadratic easing functions
    [p(x) = x^2]
"""


class QuadEaseIn(EasingBase):
    def func(self, t):
        return t*t


class QuadEaseOut(EasingBase):
    def func(self, t):
        return -(t * (t - 2))


"""
    Exponential easing functions
    [p(x) = 2^x]
"""


class ExponentialEaseIn(EasingBase):
    def func(self, t):
        if t == 0:
            return 0
        return math.pow(2, 10 * (t - 1))


class ExponentialEaseOut(EasingBase):
    def func(self, t):
        if t == 1:
            return 1
        return 1 - math.pow(2, -10 * t)


class ExponentialEaseInOut(EasingBase):
    def func(self, t):
        if t == 0 or t == 1:
            return t

        if t < 0.5:
            return 0.5 * math.pow(2, (20 * t) - 10)
        return -0.5 * math.pow(2, (-20 * t) + 10) + 1
