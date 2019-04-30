from inac8hr.scenes import Level1Scene, MainMenuScene
from inac8hr.logging import Logger
from inac8hr.events import EventDispatcher
from inac8hr.scenes import Viewport
from i18n.loc import Localization
import time


class GameEngine:

    def __init__(self):
        self.scenes = []
        self.logger = Logger()
        self.event_dispatcher = EventDispatcher()
        self.viewport = None
        self._lap_time = 0
        self.lap()
        Localization()

    def lap(self):
        self._lap_time = time.time()

    def elapsed(self):
        return time.time() - self._lap_time

    def load_all(self):
        self.logger.Log("Loading scenes")
        self.load_scenes()
        self.logger.Log("Scene initialized...")
        self.viewport = Viewport(self.scenes[0], self.event_dispatcher)
        self.logger.Log("Registering events...")

    def load_scenes(self):
        self.lap()
        MMScene = MainMenuScene()
        # self.scenes.append(MMScene)
        self.logger.Log(f"MainMenu loaded (took {self.elapsed():.5f} sec)")

        self.lap()
        Scene1 = Level1Scene()
        self.logger.Log(f"Scene 1 loaded (took {self.elapsed():.5f} sec)")
        self.scenes.append(Scene1)

