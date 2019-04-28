import arcade
import math
import pyglet
from inac8hr.hud.level1 import Level1HUD
from inac8hr.scenes.lv1_scene import Level1Scene
from inac8hr.commands import CommandHandler
from inac8hr.levels import LV1Level
from inac8hr.globals import *
from inac8hr.events import EventDispatcher
from inac8hr.scenes import Scene, Viewport
from inac8hr.layers import SceneLayer, UILayer, PlayableSceneLayer
from inac8hr.tools import ToolHandler, PlacementAvailabilityTool, UnitBlueprint
from inac8hr.globals import GAME_PREFS
from inac8hr.utils import LocationUtil
from inac8hr.anim import *
from inac8hr.imports import *
from inac8hr.utils import FPSCounter
from i18n.loc import Localization

APP_VERSION = "0.2.1"


class GameManager():
    def __init__(self, resolution):
        GAME_PREFS.scaling = 1.11
        self.fullscreen = False
        width, height = resolution
        self.screen_width = width
        self.screen_height = height
        self.activated_keys = []
        self.background = arcade.load_texture("assets/images/bck.png")
        self.fps = FPSCounter()
        self.updating = False
        self.locale = Localization()
        self.sprite_list = []
        self.state = STATE_READY
        self.dispatcher = EventDispatcher()

        self.initialize_scenes()

        self.fps_text = self.viewport.current_scene.get('ui_layer').main_element
        self.normal_text = self.viewport.current_scene.get('ui_layer').get(2)
        self.current_level = self.viewport.current_scene.get('canvas_layer').main_element

        self.tool_handler = ToolHandler(self.dispatcher)
        self.cmd_handler = CommandHandler(self)
        self.dispatcher.add_dispatcher(self.current_level)
        self.dispatcher.add_dispatcher(self.cmd_handler)
        for ctrl in self.viewport.current_scene.get('ui_layer').elements:
            self.dispatcher.add_dispatcher(ctrl)
        self.cursor_loc = 0, 0

        # self.test_sprite = PreferredSprite("assets/images/chars/avail.png", center_x=500, center_y=0)
        # self.test_sprite.alpha = 50
        # self.test_animator = SpriteAnimator(self.test_sprite, 1, animation=ExponentialEaseOut)

        self.dispatcher.register_tool_events()

    def initialize_scenes(self):
        initial_scene = Level1Scene()
        self.viewport = Viewport(initial_scene)
        print('[Logger] Scene initialized...')

    def draw(self):
        arcade.draw_texture_rectangle(self.screen_width // 2, self.screen_height // 2,
                                      self.screen_width + 500, self.screen_height + 500, self.background, alpha=255)
        self.viewport.draw()
        self.tool_handler.draw()
        # self.test_sprite.draw()

    def load_sprites(self, width, height):
        self.reset_scaling(width, height)

    def reload_sprites(self, width, height):
        self.reset_scaling(width, height)

    def reset_scaling(self, width, height):
        self.screen_width, self.screen_height = width, height
        width_ratio = width / (self.current_level.map_plan.width*GAME_PREFS.block_size)
        height_ratio = height  / (self.current_level.map_plan.height*GAME_PREFS.block_size)
        diff = math.log((((width_ratio*9) + (height_ratio*1)) / 10), 10)*2.2
        GAME_PREFS.scaling = 1 + diff

    def update(self, delta):
        self.viewport.clocked_update()
        # self.test_animator.update()
        self.fps.tick()
        self.fps_text.text = f"FPS: {self.fps.get_fps():.2f}"
        #f"Scaling: {GAME_PREFS.scaling:.2f} |
        self.normal_text.text = f"Score: {self.current_level.score} " \
        f"| {self.locale.get_translated_text('Intro/Instructions')} |-|"\
        f"{self.locale.get_translated_text('Game/Title')} dev v{APP_VERSION} |-|"
        if self.fps.get_fps() < 10:
            self.current_level.set_state(LevelState.PAUSED)

    def on_key_press(self, key, modifiers):
        self.dispatcher.on('key_press', key, modifiers)
      #  self.activated_keys.append(key)
        if key == arcade.key.ENTER:
            if self.current_level.is_playing():
                self.current_level.set_state(LevelState.PAUSED)
            else:
                self.current_level.set_state(LevelState.PLAYING)
        # elif key == arcade.key.A:
        #     self.test_animator.tween_to(500, 500)

    def on_key_release(self, key, modifiers):
        #self.activated_keys.remove(key)
        pass

    def register_sprite(self, sprite):
        "For registering a sprite to the global sprite list shared across the App"
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        self.cursor_loc = x, y
        self.dispatcher.on('mouse_motion', x, y, dx, dy)

    def on_resize(self, width, height):
        self.viewport.on_window_resize(self, width, height)
        self.reset_scaling(width, height)
        self.dispatcher.on_resize(width, height)