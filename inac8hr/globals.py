from inac8hr.settings import Preferences
from i18n.loc import Localization

GAME_PREFS = Preferences()
GAME_PREFS.block_size = 40
GAME_PREFS.scaling = 1

STATE_READY = 0
STATE_PLACEMENT = 1
MODE_PLAYING = 1
MODE_PLACING = 2

LOC_SOURCE = Localization()


class LevelState:
    PLAYING = 1
    PAUSED = 0

UNIT_FROZEN = 0
UNIT_ANIMATED = 1

DIR_STILL = 0
DIR_UP = 1
DIR_DOWN = 2
DIR_LEFT = 3
DIR_RIGHT = 4

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
    KEY_PRESS = 3
    KEY_RELEASE = 4
    WINDOW_RESIZE = 5

#
# Keymaps for each combination of pressed keys
#

KEYMAPS = {

}