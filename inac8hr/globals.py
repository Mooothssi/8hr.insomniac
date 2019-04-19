from inac8hr.settings import Preferences

GAME_PREFS = Preferences()
GAME_PREFS.block_size = 40

MODE_PLAYING = 1
MODE_PLACING = 2

#
# Indices of input events available
# 
MOUSE_PRESS = 1
MOUSE_MOTION = 2
KEY_PRESS = 3
KEY_RELEASE = 4
WINDOW_RESIZE = 5