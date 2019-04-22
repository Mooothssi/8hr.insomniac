import time
from arcade.sprite import Sprite
from inac8hr.gui import Point
from inac8hr.anim.easing import EasingBase, LinearEase


class AnimatorBase():

    def __init__(self, duration=1, animation: EasingBase=LinearEase):
        """
            Takes duration in seconds
        """
        self.duration = duration


class SpriteAnimator(AnimatorBase):

    def __init__(self, sprite: Sprite, duration=1,
                 animation: EasingBase=LinearEase):
        super().__init__(duration)
        self.start_time = time.time()
        self.sprite = sprite
        self.animation_x = animation(duration)
        self.animation_y = animation(duration)
        self.__animating__ = False

    def tween_to(self, x, y):
        start_point, endpoint = Point(self.sprite.center_x, self.sprite.center_y), Point(x, y)
        if start_point != endpoint:
            self.start_time = time.time()
            self.animation_x.start = self.sprite.center_x
            self.animation_y.start = self.sprite.center_y
            self.animation_x.end = x
            self.animation_y.end = y
            self.__animating__ = True

    def animate(self, time):
        start_x, end_x = self.animation_x.start, self.animation_x.end
        start_y, end_y = self.animation_y.start, self.animation_y.end
        x, y = self.animation_x.ease(time), self.animation_y.ease(time)
        self.sprite.set_position(x, y)

    def get_change_in_time(self):
        return time.time() - self.start_time

    def ended(self):
        return self.get_change_in_time() >= self.duration

    def update(self):
        if self.__animating__:
            alpha_time = self.get_change_in_time()
            if not self.ended():
                self.animate(alpha_time)
            else:
                self.__animating__ = False

