from inac8hr.layers import PlayableSceneLayer
from inac8hr.utils import LocationUtil
from inac8hr.globals import GAME_PREFS
from arcade.sprite import Sprite
from arcade import *
BOARD = [
        '#X################',
        '# ###    #####   #',
        '# ### ## ####  # #',
        '#     ## #### ## #',
        '######## ####  # #',
        '##       ##### # #',
        '## ##########  # #',
        '## ##      ## ## #',
        '##    #### ##  # #',
        '########## ### # #',
        '##########     # #',
        '################ #',]

DIR_UP = 1
DIR_DOWN = 2
DIR_LEFT = 3
DIR_RIGHT = 4

DIR_OFFSETS = {
    DIR_UP: (0,1),
    DIR_DOWN: (0,-1),
    DIR_LEFT: (-1,0),
    DIR_RIGHT: (1,0)
}

BLOCK_SIZE = 40

LV_PLAYING = 1
LV_PAUSED = 0

class Level(PlayableSceneLayer):
    def __init__(self):
        self.map_plan = MapPlan(BOARD, 40)
        self.defenders = []
        self.enemies = []
        self.state = LV_PAUSED
        self.scaling = 1     
        self.switch_points = []

    #
    # Arcade base overload functions
    #
    def draw(self):
        self.map_plan.draw()
        for enemy in self.enemies:
            enemy.draw()
        for defender in self.defenders:
            defender.draw()


    def clocked_update(self):
        self.map_plan.scale(GAME_PREFS.scaling)
        if self.state == LV_PAUSED:
            self.pause()
        elif self.state == LV_PLAYING:
            self.play()
    #
    #
    #

    def pause(self):
        for e in self.enemies:
            e.pause()
        for d in self.defenders:
            d.pause()

    def play(self):
        for e in self.enemies:
            e.play()
        for d in self.defenders:
            d.play()

    def set_state(self, state: int):
        self.state = state

    def place_defender(self, x, y):
        print(f"Defender placed at: {x}, {y}")


class MapPlan():
    def __init__(self, plan_list, block_size):
        self.block_size = block_size
        self.plan_array = plan_list
        self.wall_sprite = Sprite('assets/images/levels/wall - Copy.png', scale=1.11)
        self.determine_dimensions()

    def scale(self, scaling):
        self.wall_sprite = Sprite('assets/images/levels/wall - Copy.png', scale=scaling)

    def determine_dimensions(self):
        self.width = len(self.plan_array[0])
        self.height = len(self.plan_array)

    def draw(self):
        for r in range(0, self.height):
            for c in range(self.width):
                if self.is_wall_at((r,c)):
                    self.draw_sprite(self.wall_sprite, r, c)
                    #exit(0)

    def draw_sprite(self, sprite, r, c):
        x, y = LocationUtil.get_sprite_position(r, c)
        sprite.set_position(x, y)
        sprite.draw()

    def is_wall_at(self, pos):
        board = self.plan_array
        if -1 <= pos[0] <= len(board) - 1 and -1 <= pos[1] <= len(board[0]) - 1:
            if board[pos[0]][pos[1]] == '#':
                return True
            else:
                return False
        else:
            return False

    def is_obstacle_char(self, pos):
        board = self.plan_array
        if -1 <= pos[0] <= len(board) - 1 and -1 <= pos[1] <= len(board[0]) - 1:
            if board[pos[0]][pos[1]] != ' ':
                return 1
            else:
                return 0    
        else:
            return 2