import arcade
import random
from inac8hr.agents import Character

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

class World():
    def __init__(self):
        pass

class LevelDrawer():
    def __init__(self):
        self.board = BOARD
        self.enemies = []
        self.block_size = BLOCK_SIZE
        #self.character = Character('assets/images/chars/placeholder.png', self.get_initial_player_position())
        self.scaling = 1     
        self.width = len(self.board[0])
        self.height = len(self.board)
        self._is_wall_drawn = False
        self.switch_points = []
        self.defenders = []

    def load_sprites(self, scale):
        self.enemies.clear()
        self.set_scaling(scale)
        self.wall_sprite = arcade.Sprite('assets/images/levels/wall - Copy.png', scale=scale)
       

    def reload_sprites(self, scale):
        self.enemies.clear()
        self.set_scaling(scale)
        self.wall_sprite = arcade.Sprite('assets/images/levels/wall - Copy.png', scale=scale)
        self.initialize_enemies()

    def set_scaling(self, scale=1):
        self.scaling = scale
    

    def initialize_enemies(self):
        x, y = self.get_initial_player_position()
        diff = 0
        initial_pos = x + diff, y
        enemy = Character('assets/images/chars/placeholder_neutral.png', initial_pos, scaling=self.scaling)
        self.enemies.append(enemy)
        self.get_all_switch_points(enemy)

    def get_sprite_position(self, r, c):
        x = c * BLOCK_SIZE * self.scaling + ((BLOCK_SIZE * self.scaling) // 2)
        y = r * BLOCK_SIZE * self.scaling + ((BLOCK_SIZE* self.scaling) + ((BLOCK_SIZE* self.scaling) // 2))
        return x,y

    def get_initial_player_position(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 'X':
                    return (i, j)
        return (-1, -1)

    def draw_sprite(self, sprite, r, c):
        x, y = self.get_sprite_position(r, c)
        #sprite._set_position((x, y))
        sprite._position = [x,y]
        sprite.draw()

    def draw(self, scaling):
        for enemy in self.enemies:
            enemy.draw()
       # self.character.draw()
        if not self._is_wall_drawn:
            for r in range(0,self.height):
                for c in range(self.width):
                    if self.is_wall_at((r,c)):
                        self.draw_sprite(self.wall_sprite, r, c)
     #   a, b = self.character.board_position
      #  self.draw_sprite(self.character, a, b)

    def update(self, state):
        for enemy in self.enemies:
            # rand = random.randint(1,35)
            # print(f"Rand: {rand}")
            # if rand == 15:
            #     continue
            
            #self.check_collision_and_move(enemy)
            self.move_along_switches(enemy)
            enemy.update()
        #self.character.update()

    def preview_board(self):
        for line in self.board:
            print(line)

    def preview_board_specific(self, board):
        for line in board:
            print(line)

    def get_all_switch_points(self, agent):
        offsets = DIR_OFFSETS.keys()
        x, y = agent.board_position
        self.out_of_bounds = False
        board = list(self.board)
        direction = -1
        count = 0
        while not self.out_of_bounds:
            print(count) 
            count += 1
            for offset_key in offsets:
                offset = DIR_OFFSETS[offset_key]           
                check_pos = (x + offset[0], y + offset[1])
                status = self.is_obstacle_char(check_pos, board)
                if status == 0:
                    #if direction != offset_key:
                    self.switch_points.append([check_pos, offset_key])
                    line = list(board[x])
                    line[y] = '-'
                    board[x] = ''.join(line)

                    x, y = check_pos
                    direction = offset_key

                    line = list(board[check_pos[0]])
                    line[check_pos[1]] = 'X'
                    board[check_pos[0]] = ''.join(line)
                        #print("Next pos:" + str(self.position))
                elif status == 2:
                    self.out_of_bounds = True

    def check_collision_and_move(self, agent):
        offsets = DIR_OFFSETS.keys()
        for offset_key in offsets:
            offset = DIR_OFFSETS[offset_key]           
            check_pos = (agent.board_position[0] + offset[0], agent.board_position[1] + offset[1])
            if self.is_obstacle_char(check_pos, self.board) == 0:
                print("to")
                line = list(self.board[agent.board_position[0]])
                line[agent.board_position[1]] = '-'
                self.board[agent.board_position[0]] = ''.join(line)

                #self.character.board_position = check_pos
                agent.next_board_pos = check_pos
              
                # Board syncing region
                # line = list(self.board[check_pos[0]])
                # line[check_pos[1]] = 'X'
                # self.board[check_pos[0]] = ''.join(line)

               # self.preview_board()

                agent.change_direction(offset_key)
            elif self.is_obstacle_char(check_pos, self.board) == 2:
                exit()

    def move_along_switches(self, agent):
        if len(self.switch_points) == 0:
            exit()
        check_pos, offset_key = self.switch_points[0][0], self.switch_points[0][1]
        agent.next_board_pos = check_pos
        agent.change_direction(offset_key)
        if agent.check_if_overlapping():
            print("overlapped")
            self.switch_points.pop(0)

    def is_wall_at(self, pos):
        if self.board[pos[0]][pos[1]] == '#':
            return True
        else:
            return False

    def is_obstacle_char(self, pos, board):
        print((pos[0],pos[1]))
        if -1 <= pos[0] <= len(board) - 1 and -1 <= pos[1] <= len(board[0]) - 1:
            if board[pos[0]][pos[1]] != ' ':
                return 1
            else:
                return 0    
        else:
            return 2


# class TestCharRouting():
#     def __init__(self):
#         self.board = BOARD
#         self.position = self.get_player_position()

#     def get_player_position(self):
#         for i in range(len(self.board)):
#             for j in range(len(self.board[i])):
#                 if self.board[i][j] == 'X':
#                     return (i, j)
#         return (-1, -1)

#     def is_obstacle_char(self, pos):
#         if self.board[pos[0]][pos[1]] != ' ':
#             return True
#         else:
#             return False

#     def preview_board(self):
#         for line in self.board:
#             print(line)

#     def check_collision_and_move(self):
#         self.preview_board()
#         offsets = [(0,1), (1,0), (-1,0), (0,-1)]
#         for offset in offsets:
#             check_pos = (self.position[0] + offset[0], self.position[1] + offset[1])
#             if self.is_obstacle_char(check_pos):
#                 pass
#                 #print('Obs')
#                 #print(check_pos)
#                 #print('--')
#             else:
#                 print('')
#                 line = list(self.board[self.position[0]])
#                 line[self.position[1]] = '-'
#                 self.board[self.position[0]] = ''.join(line)

#                 self.position = check_pos
               
#                 line = list(self.board[check_pos[0]])
#                 line[check_pos[1]] = 'X'
#                 self.board[check_pos[0]] = ''.join(line)
#                 #print("Next pos:" + str(self.position))
                
#                 return