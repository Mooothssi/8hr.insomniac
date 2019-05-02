from inac8hr.scenes import Level1Scene, MainMenuScene
from inac8hr.logging import Logger
from inac8hr.events import EventDispatcher
from inac8hr.scenes import Viewport
from .audio import AudioEngine
from i18n.loc import Localization
import time


class GameEngine:
    _instance = None

    def __init__(self):
        self.scenes = []
        self.audio = AudioEngine.get_instance()
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
        self.logger.Intro("######### Now initializing 8HR INSOMNIAC #########")
        self.logger.Log("Loading up audio...")
        self.audio.load_sound_library()
        self.audio.add_source_from_filename("assets/audio/spoilt_ballot.wav","AGENTS/BALLOT_SPOILT_COUNTED")
        self.audio.add_source_from_filename("assets/audio/rockHit2.wav","PARTICLES/ROCK_HIT")
        self.logger.Log("Loading scenes...")
        self.viewport = Viewport(self.event_dispatcher)
        self.load_scenes()
        self.logger.Log("All scenes initialized...")
        self.logger.Log("Registering events...")

    def load_scenes(self):
        self.lap()
        MMScene = MainMenuScene()
        self.viewport.add_scene(MMScene)
        self.logger.Log(f"MainMenu loaded (took {self.elapsed():.5f} sec)")

        self.lap()
        Scene1 = Level1Scene()
        self.logger.Log(f"Scene 1 loaded (took {self.elapsed():.5f} sec)")
        self.viewport.add_scene(Scene1)
        self.viewport.choose_scene('MainScene')

    @staticmethod
    def get_instance():
        if GameEngine._instance is None:
            GameEngine._instance = GameEngine()
        return GameEngine._instance
