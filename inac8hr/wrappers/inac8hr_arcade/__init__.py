import sys

if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 6):
    sys.exit("The Arcade Library requires Python 3.6 or higher.")

from arcade import color
from arcade import key
from arcade import application, arcade_types, draw_commands, buffered_draw_commands, geometry, physics_engines, sound,sprite_list, version, window_commands, joysticks, read_tiled_map, isometric
from inac8hr.wrappers.inac8hr_arcade.sprite import *
from inac8hr.wrappers.inac8hr_arcade.legacy import *