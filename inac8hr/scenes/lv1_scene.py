from inac8hr.scenes import Scene
from inac8hr.globals import LevelState, APP_VERSION
from inac8hr.levels import LV1Level
from inac8hr.hud.level1 import Level1HUD
from inac8hr.layers import SceneLayer, UILayer, PlayableSceneLayer
from inac8hr.utils import FPSCounter
from i18n.loc import Localization


class Level1Scene(Scene):
    def __init__(self):
        self.frozen = True
        super().__init__("LV1Scene")
        self.lv1 = LV1Level()
        hud = Level1HUD(self)
        lv1_canvas = PlayableSceneLayer("canvas_layer", self.lv1)
        for i in [lv1_canvas, hud, SceneLayer("tool_layer")]:
            self.append_layer(i)
        self.fps = FPSCounter()
        self.fps_text = hud.main_element
        self.normal_text = hud.get_by_index(2)

    def freeze_canvas(self):
        self.frozen = True
        self.lv1.set_state(LevelState.PAUSED)

    def continue_canvas(self):
        self.frozen = False
        self.lv1.set_state(LevelState.PLAYING)

    def draw(self):
        super().draw()

    def tick(self):
        super().tick()
        self.fps.tick()
        self.fps_text.text = f"FPS: {self.fps.get_fps():.2f}"
        #f"Scaling: {GAME_PREFS.scaling:.2f} |
        self.normal_text.text = f"| {Localization.instance().get_translated_text('Intro/Instructions')} |-|"\
        f"{Localization.instance().get_translated_text('Game/Title')} dev v{APP_VERSION} |-|"
        if self.fps.get_fps() < 10:
            self.lv1.set_state(LevelState.PAUSED)
