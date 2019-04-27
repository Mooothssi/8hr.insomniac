#
# 8-hour
#
import time
from inac8hr.globals import DEFAULT_LIFECYCLE_TIME
from inac8hr.events import Event


class CycleClock():
    DEFAULT_CYCLES_LIMIT = 8

    def __init__(self):
        self.start_time = None
        self.current_cycle = 1
        self.limit = DEFAULT_LIFECYCLE_TIME
        self.cycle_changed = Event(self)
        self.end = False
        self.passed = 0
        self.stop_time = None
        self.paused = False

    def start(self):
        self.start_time = time.time()

    def resume(self):
        if self.paused:
            self.paused = False
            self.start()

    def pause(self):
        self.paused = True
        if self.started:
            self.passed += self.get_elapsed()
            self.start_time = None

    def stop(self):
        self.stop_time = time.time()
        self.start_time = None

    def get_elapsed(self):
        return time.time() - self.start_time

    def reset(self):
        self.start_time = None

    @property
    def started(self):
        return self.start_time is not None

    def update(self):
        if self.started and not self.paused:
            elapsed = self.get_elapsed()
            if elapsed >= self.limit:
                self.current_cycle += 1
                self.passed += elapsed
                self.start()
                self.cycle_changed()
                if self.current_cycle > self.DEFAULT_CYCLES_LIMIT:
                    self.stop()

    def __str__(self):
        return f"Cycle {self.current_cycle} | Time passed: {self.passed}s"
