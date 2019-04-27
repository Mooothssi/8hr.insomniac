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
    def __init__(self, manager, info=None):
        self.level = manager.current_level
        self.handler = manager.tool_handler
        self.manager = manager
        self.info = info

    def execute(self):
        pass


class PlacementCommand(ToolCommand):
    def __init__(self, manager, info=None):
        super().__init__(manager, info)
        self.triggered = False

    def execute(self):
        if self.triggered:
            self.handler.clear_current_tool()
            self.triggered = False
        else:
            self.handler.current_tool = PlacementAvailabilityTool(self.level, self.manager.cursor_loc)
            self.triggered = True
        # self.level.place_defender(self.info.x, self.info.y, self.info.defender)


class SelectCommand(ToolCommand):
    def __init__(self, manager, info=None):
        super().__init__(manager, info)
        self.triggered = False

    def execute(self):
        self.handler.current_tool = SelectTool(self.level)
        self.triggered = True


class CommandHandler():
    registered_inputs = [UserEvent.KEY_PRESS]

    def __init__(self, manager):
        placement = PlacementCommand(manager)
        select = SelectCommand(manager)
        self.hotkey_maps = {
            Hotkey(arcade.key.P, True): placement,
            Hotkey(arcade.key.S, True): select
        }

    def on_key_press(self, key, modifiers):
        pressed_hotkey = Hotkey(key, (modifiers & arcade.key.MOD_CTRL) > 0,
                                (modifiers & arcade.key.MOD_ALT) > 0)

        if pressed_hotkey in self.hotkey_maps:
            self.hotkey_maps[pressed_hotkey].execute()
