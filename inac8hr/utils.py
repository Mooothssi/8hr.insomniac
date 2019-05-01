import time
import collections
from inac8hr.globals import GAME_PREFS
ui_offset = 25


class LocationUtil():

    @staticmethod
    def get_sprite_position(r, c, scaling=0):
        if scaling == 0:
            product = GAME_PREFS.block_size * GAME_PREFS.scaling
        else:
            product = GAME_PREFS.block_size * scaling
        x = c * product + ((product) / 2)
        y = r * product + ((product) + ((product) / 2))
        return x, y

    @staticmethod
    def get_plan_position(x, y, rounded=False, scaling_mt=False):
        if scaling_mt:
            product = GAME_PREFS.block_size * 1
        else:
            product = GAME_PREFS.block_size * GAME_PREFS.scaling
        c = (x - (product / 2)) / product
        r = (y - (product + (product) / 2)) / product
        if rounded:
            r, c = int(round(abs(r), 0)), int(round(abs(c), 0))
        return r, c


class FPSCounter:
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=60)

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)