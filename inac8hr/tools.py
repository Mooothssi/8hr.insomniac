import arcade, math
from inac8hr.entities import UnitBlueprint, UnitInfo, VALID_PLACEMENT, INVALID_PLACEMENT
from inac8hr.utils import LocationUtil
from inac8hr.events import EventDispatcher
from inac8hr.levels import Level
from inac8hr.globals import *

class BaseTool():
    def __init__(self, level: Level, name: str="base"):
        self.level = level
        self.name = name

    def draw(self):
        pass


class PositionTool(BaseTool):
    PRX = 0.12, 0.9
    def eval_proximity(self, x, y):
        r, c = LocationUtil.get_plan_position(x, y)
        dr, dc = abs(r - math.floor(r)), abs(c - math.floor(c))
        if (0 <= dc <= self.PRX[0] or self.PRX[1] <= dc < 1) and (0 <= dr <= self.PRX[0] or self.PRX[1] <= dr < 1):
            return True
        else:
            return False


class UnitPlacementTool(PositionTool):
    registered_inputs = [UserEvent.MOUSE_PRESS, UserEvent.MOUSE_MOTION,
                         UserEvent.WINDOW_RESIZE]

    def __init__(self, level: Level, initial_loc=(0, 0)):
        super().__init__(level, "placement")
        self.unit_blueprint = UnitBlueprint(["assets/images/chars/unavail.png", "assets/images/chars/avail.png"], scaling=GAME_PREFS.scaling, initial_loc=initial_loc)
        self.unit_blueprint.sprite.scale = GAME_PREFS.scaling
        self.current_cursor_pos = initial_loc

    def eval_availability(self, x, y):
        if self.eval_proximity(x, y):
            r, c = LocationUtil.get_plan_position(x, y, True)
            return self.level.map_plan.is_wall_at((r, c)) and not self.level.is_defender_at(r, c)
        else:
            return False

    def update_blueprint_state(self, x, y):
        if self.eval_availability(x, y):
            self.unit_blueprint.change_state(1)
        else:
            self.unit_blueprint.change_state(0)

    def change_blueprint(self, blueprint_info: UnitInfo):
        self.unit_blueprint = blueprint_info.blueprint
        self.unit_blueprint.sprite.set_position(self.current_cursor_pos[0], self.current_cursor_pos[1])

    def on_mouse_motion(self, *args):
        x, y, dx, dy = args
        self.current_cursor_pos = x, y
        self.unit_blueprint.sprite.set_position(x, y)
        self.update_blueprint_state(x, y)

    def on_mouse_press(self, *args):
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


class SelectTool(PositionTool):
    registered_inputs = [UserEvent.MOUSE_PRESS]

    def __init__(self, level: Level):
        super().__init__(level, "select")
        self.selection = None
        self.PRX = 0.4, 0.6

    def eval_availability(self, x, y):
        if self.eval_proximity(x, y):
            r, c = LocationUtil.get_plan_position(x, y, True)
            return self.level.is_defender_at(r, c)
        else:
            return False

    def on_mouse_press(self, *args):
        x, y, button, modifiers = args
        if self.eval_availability(x, y):
            r, c = LocationUtil.get_plan_position(x, y, True)
            selection = self.level.get_defender_at(r, c)
            if selection != self.selection:
                if self.selection is not None:
                    self.selection.on_selection(False)
                self.selection = selection
            self.selection.on_selection(button == arcade.MOUSE_BUTTON_LEFT)
            print(self.level.get_defender_at(r, c))


class ToolHandler():
    registered_inputs = [UserEvent.MOUSE_MOTION]

    def __init__(self, event_dispatcher: EventDispatcher, model: Level):
        self.tools = []
        self.level = model
        self.dispatcher = event_dispatcher
        self.cursor_loc = (0, 0)
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

    def is_tool_utilized(self, tool_name: str) -> bool:
        if self.current_tool is None:
            return False
        else:
            return self.current_tool.name == tool_name

    def draw(self):
        if self.__current_tool__ is not None:
            self.current_tool.draw()
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor_loc = x, y

    current_tool = property(get_current_tool, set_current_tool)