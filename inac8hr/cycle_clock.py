#
# 8-hour
#
import time
from inac8hr.globals import *


class CycleClock():
    def __init__(self):
        self.start = None
        self.limit = DEFAULT_LIFECYCLE_TIME

    def start(self):
        self.start = time.time()

    def get_elapsed(self):
        delta_time = time.time() - self.start

    def reset(self):
        self.start = None


