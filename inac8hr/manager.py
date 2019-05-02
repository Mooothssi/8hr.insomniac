import arcade
import math
import pyglet
from inac8hr.engines import GameEngine
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
from i18n.loc import Localization


class GameManager():
    def __init__(self, resolution):
        # GAME_PREFS.scaling = 1.11
        self.fullscreen = False
        width, height = resolution
        self.screen_width = width
        self.screen_height = height
        self.activated_keys = []
        self.background = arcade.load_texture("assets/images/bck.png")
        self.updating = False
        self.sprite_list = []
        self.state = STATE_READY
        self.engine = GameEngine.get_instance()
        self.engine.load_all()
        self.dispatcher = self.engine.event_dispatcher
        self.viewport = self.engine.viewport
        self.current_level = self.viewport.get('LV1Scene').get('ui_layer').lv1
        self.cursor_loc = 0, 0

        # self.test_sprite = PreferredSprite("assets/images/chars/avail.png", center_x=500, center_y=0)
        # self.test_sprite.alpha = 50
        # self.test_animator = SpriteAnimator(self.test_sprite, 1, animation=ExponentialEaseOut)

        # self.dispatcher.register_tool_events()

    def draw(self):
        arcade.draw_texture_rectangle(self.screen_width // 2, self.screen_height // 2,
                                      self.screen_width + 500, self.screen_height + 500, self.background, alpha=255)
        self.viewport.draw()

    def load_sprites(self, width, height):
        self.reset_scaling(width, height)

    def reload_sprites(self, width, height):
        self.reset_scaling(width, height)

    def reset_scaling(self, width, height):
        GAME_PREFS.screen_width, GAME_PREFS.screen_height = width, height
        self.screen_width, self.screen_height = width, height
        width_ratio = width / (self.current_level.map_plan.width*GAME_PREFS.block_size)
        height_ratio = height  / (self.current_level.map_plan.height*GAME_PREFS.block_size)
        diff = math.log((((width_ratio*9) + (height_ratio*1)) / 10), 10)*2.2
        GAME_PREFS.scaling = 1 + diff

    def update(self, delta):
        self.viewport.tick()

    def on_key_press(self, key, modifiers):
        self.dispatcher.on('key_press', key, modifiers)
      #  self.activated_keys.append(key)
        # if key == arcade.key.ENTER:
        #     if self.current_level.is_playing():
        #         self.current_level.set_state(LevelState.PAUSED)
        #     else:
        #         self.current_level.set_state(LevelState.PLAYING)
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
        self.reset_scaling(width, height)
        self.viewport.on_window_resize(self, width, height)

