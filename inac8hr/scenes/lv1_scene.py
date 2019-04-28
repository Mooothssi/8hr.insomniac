from inac8hr.scenes import Scene
from inac8hr.globals import LevelState
from inac8hr.levels import LV1Level
from inac8hr.hud.level1 import Level1HUD
from inac8hr.layers import SceneLayer, UILayer, PlayableSceneLayer


class Level1Scene(Scene):
    def __init__(self):
        self.frozen = True
        self.lv1 = LV1Level()
        lv1_canvas = PlayableSceneLayer("canvas_layer", self.lv1)
        super().__init__(lv1_canvas, Level1HUD(self), SceneLayer("tool_layer"))

    def freeze_canvas(self):
        self.frozen = True
        self.lv1.set_state(LevelState.PAUSED)

    def continue_canvas(self):
        self.frozen = False
        self.lv1.set_state(LevelState.PLAYING)
