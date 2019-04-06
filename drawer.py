import arcade
import random

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


    def load_sprites(self, scale):
        self.set_scaling(scale)
        self.wall_sprite = arcade.Sprite('assets/images/levels/wall.png', scale=scale)
        self.initialize_enemies()


    def set_scaling(self, scale=1):
        self.scaling = scale
    

    def initialize_enemies(self):
        x, y = self.get_initial_player_position()
        for diff in range(2):
            initial_pos = x + diff, y
            enemy = Character('assets/images/chars/placeholder.png', initial_pos, scaling=self.scaling)
            self.enemies.append(enemy)

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
        sprite.set_position(x, y)
        sprite.draw()

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()
       # self.character.draw()
        for r in range(0,self.height):
            for c in range(self.width):
                if self.is_wall_at((r,c)):
                    self.draw_sprite(self.wall_sprite, r, c)
     #   a, b = self.character.board_position
      #  self.draw_sprite(self.character, a, b)

    def update(self):
        for enemy in self.enemies:
            # rand = random.randint(1,35)
            # print(f"Rand: {rand}")
            # if rand == 15:
            #     continue
            self.check_collision_and_move(enemy)
            enemy.update()
        #self.character.update()

    def preview_board(self):
        for line in self.board:
            print(line)

    def check_collision_and_move(self, agent):
        offsets = DIR_OFFSETS.keys()
        
        for offset_key in offsets:
            offset = DIR_OFFSETS[offset_key]           
            check_pos = (agent.board_position[0] + offset[0], agent.board_position[1] + offset[1])
            print(check_pos)
            if not self.is_obstacle_char(check_pos):
                print("to")
                line = list(self.board[agent.board_position[0]])
                line[agent.board_position[1]] = '-'
                self.board[agent.board_position[0]] = ''.join(line)
                # TODO: add sprite velocity
                #self.character.board_position = check_pos
                agent.next_board_pos = check_pos
              
                # Board syncing region
                # line = list(self.board[check_pos[0]])
                # line[check_pos[1]] = 'X'
                # self.board[check_pos[0]] = ''.join(line)

               # self.preview_board()

                agent.change_direction(offset_key)

    def is_wall_at(self, pos):
        if self.board[pos[0]][pos[1]] == '#':
            return True
        else:
            return False

    def is_obstacle_char(self, pos):
        if self.board[pos[0]][pos[1]] != ' ':
            return True
        else:
            return False

class Character():
    def __init__(self, sprite_name, pos, scaling=1):
        self.sprite = arcade.Sprite(sprite_name)
        self.board_position = pos
        self.next_board_pos = (0,0)
        self.scaling = scaling
        sp_pos_x, sp_pos_y = self.get_sprite_position(pos[0], pos[1])
        self.sprite.set_position(sp_pos_x, sp_pos_y)
        self.sprite.width = 50
        self.sprite.height = 50
        self.next_direction = DIR_UP
        #print(pos)

    def check_in_place(self):
        r, c = self.next_board_pos
        next_x, next_y = self.get_sprite_position(r, c)
       # print(f'Next pos: {(next_x, next_y)}')
        curr_x, curr_y = self.sprite.position
        return (curr_x - next_x)*DIR_OFFSETS[self.next_direction][1] >= 0 and (curr_y - next_y)*DIR_OFFSETS[self.next_direction][0] >= 0



    def get_sprite_position(self, r, c):
        x = c * BLOCK_SIZE * self.scaling + ((BLOCK_SIZE * self.scaling) // 2)
        y = r * BLOCK_SIZE * self.scaling + ((BLOCK_SIZE* self.scaling) + ((BLOCK_SIZE* self.scaling) // 2))
        return x,y

    def change_direction(self, direction):
        print(self.next_direction)
      
        self.next_direction = direction

    def move(self):
        if self.check_in_place():
            self.board_position = self.next_board_pos
            reset_pos_x, reset_pos_y = self.get_sprite_position(self.board_position[0],self.board_position[1])
            self.set_position(reset_pos_x, reset_pos_y)
        else:
            x, y = self.sprite.position[0], self.sprite.position[1]#self.get_sprite_position(self.board_position[0], self.board_position[1])
            rand_velc = 2.5 #(random.randint(1,20)/20)
            self.set_position(x + DIR_OFFSETS[self.next_direction][1]*rand_velc, y + DIR_OFFSETS[self.next_direction][0]*rand_velc)
        #print(f'Curr pos: {self.sprite.position}')

    def update(self):
        self.move()
        #self.draw()

    def draw(self):
        self.sprite.draw()

    def set_position(self, x, y):
        self.sprite.set_position(x, y)


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