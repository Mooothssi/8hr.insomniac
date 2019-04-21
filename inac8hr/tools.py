import arcade, math
from inac8hr.utils import LocationUtil
from inac8hr.inputs import EventDispatcher
from inac8hr.levels import Level
from inac8hr.globals import *

VALID_PLACEMENT = 1
INVALID_PLACEMENT = 0


class BaseTool():
    def draw(self):
        pass


class PlacementAvailabilityTool(BaseTool):
    registered_inputs = [MOUSE_PRESS, MOUSE_MOTION, WINDOW_RESIZE]

    def __init__(self, level: Level, initial_loc=(0, 0)):
        self.unit_blueprint = UnitBlueprint(["assets/images/chars/unavail.png","assets/images/chars/avail.png"], scaling=GAME_PREFS.scaling, initial_loc=initial_loc)
        self.unit_blueprint.sprite.scale = GAME_PREFS.scaling
        self.level = level

    def update_blueprint_state(self, x, y):
        if self.eval_availability(x, y):
            self.unit_blueprint.change_state(1)
        else:
            self.unit_blueprint.change_state(0)
    
    def eval_availability(self, x, y):
        if self.eval_proximity(x, y):
            r, c = LocationUtil.get_plan_position(x, y)
            r, c = int(round(abs(r),0)), int(round(abs(c),0))
            return self.level.map_plan.is_wall_at((r, c)) and not self.level.is_defender_at(r, c)
        else:
            return False

    def eval_proximity(self, x, y):
        r, c = LocationUtil.get_plan_position(x, y)
        if ( 0 <=  abs( c - math.floor(c)) <= 0.1 or 0.92 <=  abs( c - math.floor(c)) < 1) and (0 <= abs( r - math.floor(r)) <= 0.1 or 0.92 <=  abs( r - math.floor(r)) < 1):
            return True
        else:
            return False

    def on_mouse_motion(self, args: tuple):
        x, y, dx, dy = args
        self.unit_blueprint.sprite.set_position(x, y)
        self.update_blueprint_state(x, y)

    def on_mouse_press(self, args: tuple):
        x, y, button, modifiers = args
        if self.eval_availability(x, y):
            self.unit_blueprint.location = LocationUtil.get_plan_position(x,y, True)
            r, c = self.unit_blueprint.location
            self.level.place_defender(r, c)
            self.unit_blueprint.change_state(INVALID_PLACEMENT)

    def on_resize(self):
        self.unit_blueprint.rescale()
   
    def draw(self):
        self.unit_blueprint.sprite.draw()


class UnitBlueprint():
    "Minimum of 2 texture files"
    def __init__(self, texture_files: list, scaling=1, initial_loc=(0,0)):
        self.defender = None
        self.sprite = arcade.Sprite()
        self.texture_files = texture_files
        for file_name in texture_files:
            self.sprite.append_texture(arcade.load_texture(file_name))
        self.state = INVALID_PLACEMENT
        self.configure_texture()
        self.position = initial_loc

    def set_position(self, value):
        self.sprite.set_position(*value)
    
    def get_position(self):
        return self.sprite.position
    
    position = property(get_position, set_position)

    def rescale(self):
        self.configure_texture()

    def configure_texture(self):
        self.sprite.scale = GAME_PREFS.scaling
        self.sprite.set_texture(self.state)

    def change_state(self, state):
        self.state = state
        self.configure_texture()


class UnitPlacement():

    def check_availability(self):
        pass


class ToolHandler():
    registered_inputs = [MOUSE_MOTION]
    def __init__(self, event_dispatcher: EventDispatcher):
        self.tools = []
        self.dispatcher = event_dispatcher
        self.__current_tool__ = None

    def get_current_tool(self):
        return self.__current_tool__

    def set_current_tool(self, tool: BaseTool):
        if self.__current_tool__ is not None:
            self.dispatcher.deregister_dispatcher(self.__current_tool__)
        self.__current_tool__ = tool
        if self.__current_tool__ is not None:
            self.dispatcher.register_dispatcher(self.__current_tool__)

    def add_tool(self, tool: BaseTool):
        self.tools.append(tool)
   
    def clear_current_tool(self):
        self.current_tool = None

    def draw(self):
        if self.__current_tool__ is not None:
            self.current_tool.draw()

    current_tool = property(get_current_tool, set_current_tool)