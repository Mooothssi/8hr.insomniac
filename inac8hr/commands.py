import arcade
from inac8hr.tools import BaseTool, SelectTool, PlacementAvailabilityTool
from inac8hr.events import Hotkey
from inac8hr.globals import UserEvent


class PlacementInfo():
    def __init__(self, x, y, defender):
        self.x = x
        self.y = y
        self.defender = defender


class Action():
    pass


class BaseCommand(Action):
    def __init__(self, args):
        pass

    def execute(self):
        pass


class ToolCommand(BaseCommand):
    def __init__(self, handler, info=None):
        self.handler = handler
        self.info = info

    def execute(self):
        pass


class PlacementCommand(ToolCommand):
    def __init__(self, handler, info=None):
        super().__init__(handler, info)
        self.triggered = False

    def execute(self):
        if self.triggered:
            self.handler.clear_current_tool()
            self.triggered = False
        else:
            self.handler.current_tool = PlacementAvailabilityTool(self.handler.level, self.handler.cursor_loc)
            self.triggered = True
        # self.level.place_defender(self.info.x, self.info.y, self.info.defender)


class SelectCommand(ToolCommand):
    def __init__(self, handler, info=None):
        super().__init__(handler, info)
        self.triggered = False

    def execute(self):
        self.handler.current_tool = SelectTool(self.handler.level)
        self.triggered = True


class CommandHandler():
    registered_inputs = [UserEvent.KEY_PRESS]

    def __init__(self, tool_handler):
        self.hotkey_maps = {
            Hotkey(arcade.key.P, True): PlacementCommand(tool_handler),
            Hotkey(arcade.key.S, True): SelectCommand(tool_handler)
        }
        self.str_maps = {
            "placement": PlacementCommand(tool_handler),
            "select": SelectCommand(tool_handler)
        }

    def execute_by_keyword(self, keyword: str):
        self.str_maps[keyword].execute()

    def on_key_press(self, key, modifiers):
        pressed_hotkey = Hotkey(key, (modifiers & arcade.key.MOD_CTRL) > 0,
                                (modifiers & arcade.key.MOD_ALT) > 0)

        if pressed_hotkey in self.hotkey_maps:
            self.hotkey_maps[pressed_hotkey].execute()
