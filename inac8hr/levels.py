from inac8hr.layers import PlayableSceneLayer
from inac8hr.utils import LocationUtil
from inac8hr.globals import GAME_PREFS, WINDOW_RESIZE
from inac8hr.units import DefenderUnit, AgentUnit
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
    registered_inputs = [WINDOW_RESIZE]
    def __init__(self):
        self.map_plan = MapPlan(BOARD, 40)
        self.defenders = {}
        self.enemies = []
        self.state = LV_PLAYING
        self.scaling = 1     
        self.generate_enemies()

    #
    # Arcade base overload functions
    #
    def draw(self):
        for enemy in self.enemies:
            enemy.draw()
        self.map_plan.draw()
        for defender in self.defenders.values():
            defender.draw()
        
        


    def clocked_update(self):
        self.on_resize()
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
        for d in self.defenders.values():
            d.pause()

    def play(self):
        for e in self.enemies:
            e.play()
        for d in self.defenders.values():
            d.play()

    def set_state(self, state: int):
        self.state = state

    def generate_enemies(self):
        x, y = self.map_plan.get_initial_agent_position()
        diff = 0
        initial_pos = x + diff, y
        enemy = AgentUnit('assets/images/chars/placeholder_neutral.png', initial_pos, self.scaling, self.map_plan.switch_points)
        self.enemies.append(enemy)

    def place_defender(self, x, y):
        self.defenders[(x,y)] = DefenderUnit("assets/images/chars/avail.png", (x,y), GAME_PREFS.scaling)

    def is_defender_at(self, x, y):
        return (x,y) in self.defenders

    def on_resize(self):
        self.scaling = GAME_PREFS.scaling
        self.map_plan.scale(GAME_PREFS.scaling)
        for defender in self.defenders.values():
            defender.scale(GAME_PREFS.scaling)


class MapPlan():
    def __init__(self, plan_list, block_size):
        self.block_size = block_size
        self.plan_array = plan_list
        self.switch_points = []
        self.scale(1)
        self.determine_dimensions()
        self.calculate_all_switch_points()

    def scale(self, scaling):
        self.wall_sprite = Sprite('assets/images/levels/wall - Copy.png', scale=scaling)

    def determine_dimensions(self):
        self.width = len(self.plan_array[0])
        self.height = len(self.plan_array)

    def calculate_all_switch_points(self):
        x, y = self.get_initial_agent_position()
        out_of_bounds = False
        board = list(self.plan_array)
        while not out_of_bounds:
            for offset_key in DIR_OFFSETS.keys():
                x_offset, y_offset = DIR_OFFSETS[offset_key]           
                check_pos = (x + x_offset, y + y_offset)
                status = self.is_obstacle_char(check_pos, board)
                if status == 0:
                    self.switch_points.append([check_pos, offset_key])
                    line = list(board[x])
                    line[y] = '-'
                    board[x] = ''.join(line)

                    x, y = check_pos

                    line = list(board[check_pos[0]])
                    line[check_pos[1]] = 'X'
                    board[check_pos[0]] = ''.join(line)

                elif status == 2:
                    out_of_bounds = True

    def get_initial_agent_position(self):
        for i in range(len(self.plan_array)):
            for j in range(len(self.plan_array[i])):
                if self.plan_array[i][j] == 'X':
                    return (i, j)
        return (-1, -1)

    def draw(self):
        for r in range(0, self.height):
            for c in range(self.width):
                if self.is_wall_at((r,c)):
                    self.draw_sprite(self.wall_sprite, r, c)

    def draw_sprite(self, sprite, r, c):
        x, y = LocationUtil.get_sprite_position(r, c)
        sprite.set_position(x, y)
        sprite.draw()

    def is_wall_at(self, pos):
        board = self.plan_array
        if -1 <= pos[0] <= len(board) - 1 and -1 <= pos[1] <= len(board[0]) - 1:
            return board[pos[0]][pos[1]] == '#'
        else:
            return False

    def is_obstacle_char(self, pos, board):
        if -1 <= pos[0] <= len(board) - 1 and -1 <= pos[1] <= len(board[0]) - 1:
            if board[pos[0]][pos[1]] != ' ':
                return 1
            else:
                return 0    
        else:
            return 2