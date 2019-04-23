import time
from arcade.sprite import Sprite
from inac8hr.gui import Point
from inac8hr.anim.sequences import SceneSequence
from inac8hr.anim.easing import EasingBase, LinearEase


class AnimatorBase():

    def __init__(self, duration=1, animation: EasingBase=LinearEase):
        """
            Takes duration in seconds
        """
        self.duration = duration
        self.start_time = time.time()
        self.elapsed = 0
        self.__animating__ = False
    
    def get_elapsed(self):
        """
            in seconds
        """
        self.elapsed = time.time() - self.start_time
        return self.elapsed

    def ended(self):
        return self.get_elapsed() >= self.duration


class SpriteAnimator(AnimatorBase):

    def __init__(self, sprite: Sprite, duration=1,
                 animation: EasingBase=LinearEase):
        super().__init__(duration)
        self.sprite = sprite
        self.animation_x = animation(duration)
        self.animation_y = animation(duration)

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
        x, y = self.animation_x.ease(time), self.animation_y.ease(time)
        self.sprite.set_position(x, y)

    def update(self):
        if self.__animating__:
            alpha_time = self.get_elapsed()
            if not self.ended():
                self.animate(alpha_time)
            else:
                self.__animating__ = False

class ControlAnimator(AnimatorBase):
    def __init__(self, duration=1, sequences=[]):
        super().__init__()
        self.start_time = time.time()
        self.animations = []
        self.sequences = []
        self.__current_sequence__ = 0

    def add_sequence(self, seq):
        self.sequences.append(seq)

    def start(self):
        if len(self.sequences) > 0:
            self.__animating__ = True

    @property
    def current_sequence(self):
        return self.sequences[self.__current_sequence__]
  
    def ended(self):
        return self.get_elapsed() >= self.current_sequence.duration

    def next(self):
        self.__current_sequence__ += 1

    def update(self):
        if self.__animating__:
            alpha_time = self.get_elapsed()
            if not self.ended():
                self.current_sequence.animate(alpha_time)
            else:
                if self.current_sequence.start_behaviour == SceneSequence.TIME_CONTROLLED and self.__current_sequence__ != len(self.sequences) - 1:
                    self.start_time = time.time()
                    self.next()
                else:
                    self.__animating__ = False
