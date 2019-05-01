from inac8hr.scenes import Scene
from inac8hr.hud import MainMenuLayer


class MainMenuScene(Scene):
    def __init__(self):
        super().__init__("MainScene")
        self.append_layer(MainMenuLayer())
