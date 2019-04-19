from inac8hr.layers import PlayableSceneLayer

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
        self.board = BOARD
        self.map_plan = None
        self.defenders = []
        self.enemies = []
        self.state = LV_PAUSED
        self.scaling = 1     
        self.initialize_board()
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
        if self.state == LV_PAUSED:
            self.pause()
        elif self.state == LV_PLAYING:
            self.play()
    #
    #
    #

    def initialize_board(self):
        self.width = len(self.board[0])
        self.height = len(self.board)

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


class MapPlan():
    def __init__(self, plan_list, block_size):
        self.block_size = block_size
        self.plan_array = plan_list
        self.determine_dimensions()

    def determine_dimensions(self):
        self.width = len(self.plan_array[0])
        self.height = len(self.plan_array)

    def draw(self):
        for r in range(0, self.height):
            for c in range(self.width):
                if self.is_wall_at((r,c)):
                    pass
                    #self.draw_sprite(self.wall_sprite, r, c)

    def is_wall_at(self, pos):
        if self.plan_array[pos[0]][pos[1]] == '#':
            return True
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