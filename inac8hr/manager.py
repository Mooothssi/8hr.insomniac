import arcade
import collections
import time
from inac8hr.agents import Character
from inac8hr.levels import Level
from inac8hr.inputs import EventDispatcher
from inac8hr.scenes import Scene, Viewport
from inac8hr.layers import SceneLayer, PlayableSceneLayer
from inac8hr.tools import PlacementAvailabilityTool, UnitBlueprint
from inac8hr.drawer import LevelDrawer#, Character
from inac8hr.globals import GAME_PREFS
from inac8hr.utils import *
from i18n.loc import Localization

APP_VERSION = "0.1.2"
STATE_READY = 0
STATE_PLACEMENT = 1

class FPSCounter:
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=60)

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)

class GameManager():
    DIR_DELTA = {
        arcade.key.UP: (0,1),
        arcade.key.DOWN: (0,-1),
        arcade.key.LEFT: (-1,0),
        arcade.key.RIGHT: (1, 0),
    }
    def __init__(self, resolution):
        GAME_PREFS.scaling = 1.11
        self.drawer = LevelDrawer()
        self.fullscreen = False
        width, height = resolution
        self.screen_width = width
        self.screen_height = height
        self.activated_keys = []
        self.character_moving = False
        self.background = arcade.load_texture("assets/images/bck.png")
        self.cursor = Character('assets/images/chars/avail.png',(-5,-5))
        self.cursor_pos = (0,0)
        self.cursor.sprite.scale = 0.5
        self.cursor.sprite.alpha = 0.5
        self.fps = FPSCounter()
        self.updating = False
        self.locale = Localization()
        self.sprite_list = []
        self.state = STATE_READY
        self.dispatcher = EventDispatcher()

        self.initialize_scenes()

        self.current_tool = PlacementAvailabilityTool(self.viewport.current_scene.get('canvas_layer').main_element)
        self.dispatcher.add_dispatcher(self.current_tool)
        self.dispatcher.add_dispatcher(self.viewport.current_scene.get('canvas_layer').main_element)

        self.dispatcher.register_tool_events()

    def initialize_scenes(self):
        level_1 = Level()
        level_1_scene = PlayableSceneLayer("canvas_layer", level_1)
        initial_scene = Scene(level_1_scene, SceneLayer("ui_layer"), SceneLayer("tool_layer"))
        self.viewport = Viewport(initial_scene)

    def draw(self):
        arcade.draw_texture_rectangle(self.screen_width // 2, self.screen_height // 2, self.screen_width + 500, self.screen_height + 500, self.background)
        self.viewport.draw()
        self.current_tool.draw()
        #arcade.draw_text("3",0,0,arcade.color.BLACK)
        arcade.draw_text(f"FPS: {self.fps.get_fps():.2f} | Scaling: {GAME_PREFS.scaling:.2f} | Score: {0} | {self.locale.get_translated_text('Intro/Instructions')} |-| {self.locale.get_translated_text('Game/Title')} dev v{APP_VERSION} |-|", 16, 8, arcade.color.BLACK )

    def load_sprites(self, width, height):
       # if not self.character_moving:
        self.reset_scaling(width, height)
        self.drawer.load_sprites(GAME_PREFS.scaling)
       # self.drawer.get_all_switch_points(self.drawer.enemies[0])

    def reload_sprites(self, width, height):
       # if not self.character_moving:
        self.reset_scaling(width, height)
        self.drawer.reload_sprites(GAME_PREFS.scaling)
        
    def reset_scaling(self, width, height):
        self.screen_width, self.screen_height = width, height
        import math
        width_ratio = width / (self.drawer.width*self.drawer.block_size)
        height_ratio = height  / (self.drawer.height*self.drawer.block_size)
        diff = math.log((((width_ratio*9) + (height_ratio*1)) / 10), 10)*2.2
        GAME_PREFS.scaling = 1 + diff

    def update(self, delta):
        self.viewport.clocked_update()
        #print(1/delta)

        #self.drawer.check_collision_and_move(self.drawer.character)
        level_state = self.character_moving
        self.drawer.update(level_state)
        #self.unit_blueprint.sprite.center_x,  self.unit_blueprint.sprite.center_y = self.cursor_pos[0],self.cursor_pos[1]
        self.fps.tick()
        # if self.character_moving:
        #     self.drawer.character.set_position(self.drawer.character.center_x + self.DIR_DELTA[self.activated_keys[0]][0], self.drawer.character.center_y + self.DIR_DELTA[self.activated_keys[0]][1])

    def on_key_press(self, key, modifiers):
        self.activated_keys.append(key)
        print(key)
        print("down")
        if key == arcade.key.ENTER:
            self.character_moving = not self.character_moving

    def on_key_release(self, key, modifiers):
        #self.character_moving = False
        self.activated_keys.remove(key)
        print(key)
        print("up")

    def on_mouse_press(self, x, y, button, modifiers):
        self.dispatcher.on_mouse_press(x, y, button, modifiers)

    def register_sprite(self, sprite):
        "For registering a sprite to the global sprite list across the App"
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        self.dispatcher.on_mouse_motion(x, y, dx, dy)

    def on_resize(self, width, height):
        self.reset_scaling(width, height)
        self.dispatcher.on_resize(width, height)