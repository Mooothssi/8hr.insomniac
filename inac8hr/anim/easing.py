import math
from abc import abstractmethod


class EasingBase:
    """
        Based on Penner's easing (gentle motion) functions
        Adapted from Semitable's version(https://github.com/semitable/easing-functions)

        Args:
            start (int): The start position of the function
            end (int): The end position of the function (multiplier)
            duration (int): Time duration of easing
    """
    __slots__ = ("start", "end", "duration", "reverse")
    limit = (0, 1)

    def __init__(self, start=0, end=1, duration=1):
        self.start = start
        self.end = end
        self.duration = duration
        self.reverse = False
        if start > end:
            self.start = end
            self.end = start
            self.reverse = True

    @abstractmethod
    def func(self, t):
        pass

    def ease(self, alpha):
        curr_t = self.limit[0] * (1 - alpha) + self.limit[1] * alpha
        if self.reverse:
            t = self.duration - curr_t
            if alpha >= self.duration:
                return self.end
        else:
            t = curr_t
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
    Quintic easing functions
    [p(x) = x^5]
"""


class QuinticEaseIn(EasingBase):
    def func(self, t):
        return t * t * t * t * t


class QuinticEaseOut(EasingBase):
    def func(self, t):
        return (t - 1) * (t - 1) * (t - 1) * (t - 1) * (t - 1) + 1


class QuinticEaseInOut(EasingBase):
    def func(self, t):
        if t < 0.5:
            return 16 * t * t * t * t * t
        p = ((2 * t) - 2)
        return 0.5 * p * p * p * p * p + 1


"""
    Sine easing functions
    [p(x) = sin(x)]
"""


class SineEaseIn(EasingBase):
    def func(self, t):
        return math.sin((t - 1) * math.pi / 2) + 1


class SineEaseOut(EasingBase):
    def func(self, t):
        return math.sin(t * math.pi / 2)


class SineEaseInOut(EasingBase):
    def func(self, t):
        return 0.5 * (1 - math.cos(t * math.pi))


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


"""
    Elastic Easing Functions
    [p(x) = sin(x), damped]
"""


class ElasticEaseIn(EasingBase):
    def func(self, t):
        return math.sin(13 * math.pi / 2 * t) * math.pow(2, 10 * (t - 1))


class ElasticEaseOut(EasingBase):
    def func(self, t):
        return math.sin(-13 * math.pi / 2 * (t + 1)) * math.pow(2, -10 * t) + 1


class ElasticEaseInOut(EasingBase):
    def func(self, t):
        if t < 0.5:
            return 0.5*math.sin(13*math.pi / 2*(2*t))*math.pow(2, 10*((2*t)-1))
        return 0.5*(math.sin(-13*math.pi/2*((2*t-1)+1))*math.pow(2, -10*(2*t-1)) + 2)


"""
    Back Easing Functions
"""


class BackEaseIn(EasingBase):
    def func(self, t):
        return t * t * t - t * math.sin(t * math.pi)


class BackEaseOut(EasingBase):
    def func(self, t):
        p = 1 - t
        return 1 - (p * p * p - p * math.sin(p * math.pi))


class BackEaseInOut(EasingBase):
    def func(self, t):
        if t < 0.5:
            p = 2 * t
            return 0.5 * (p * p * p - p * math.sin(p * math.pi))

        p = (1 - (2 * t - 1))

        return 0.5 * (1 - (p * p * p - p * math.sin(p * math.pi))) + 0.5
