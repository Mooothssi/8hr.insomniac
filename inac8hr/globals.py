import arcade
from inac8hr.settings import Preferences
from i18n.loc import Localization

APP_VERSION = "0.2.1"

DEFAULT_LIFECYCLE_TIME = 55

GAME_PREFS = Preferences()
GAME_PREFS.block_size = 40
GAME_PREFS.scaling = 1
GAME_PREFS.screen_width = 800
GAME_PREFS.screen_height = 600

STATE_READY = 0
STATE_PLACEMENT = 1
MODE_PLAYING = 1
MODE_PLACING = 2

LOC_SOURCE = Localization()


class LevelState:
    PLAYING = 1
    PAUSED = 0


DIR_STILL = 0
DIR_UP = 8
DIR_DOWN = 4
DIR_LEFT = 2
DIR_RIGHT = 1

DIR_OFFSETS = {
    DIR_UP: (0, 1),
    DIR_DOWN: (0, -1),
    DIR_LEFT: (-1, 0),
    DIR_RIGHT: (1, 0),
    DIR_STILL: (0, 0)
}


class UserEvent:
    """
        Indices of input events available
    """
    MOUSE_PRESS = 1
    MOUSE_MOTION = 2
    MOUSE_RELEASE = 3
    MOUSE_SCROLL = 4
    KEY_PRESS = 5
    KEY_RELEASE = 6
    WINDOW_RESIZE = 7

#
# Keymaps for each combination of pressed keys
#

KEYMAPS = {

}


