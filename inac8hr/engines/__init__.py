from inac8hr.scenes.lv1_scene import Level1Scene
from inac8hr.logging import Logger
from inac8hr.scenes import Viewport
import time


class GameEngine:
    def __init__(self):
        self.scenes = []
        self.logger = Logger()
        self.viewport = None
        self._lap_time = 0
        self.lap()

    def lap(self):
        self._lap_time = time.time()

    def elapsed(self):
        return time.time() - self._lap_time

    def load_all(self):
        self.logger.Log("Loading scenes")
        self.load_scenes()
        self.logger.Log("Scene initialized...")
        self.viewport = Viewport(self.scenes[0])

    def load_scenes(self):
        self.lap()
        Scene1 = Level1Scene()
        self.logger.Log(f"Scene 1 loaded (took {self.elapsed():.5f} sec)")
        self.scenes.append(Scene1)
