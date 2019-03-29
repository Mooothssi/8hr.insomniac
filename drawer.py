import arcade

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


class LevelDrawer(arcade.Sprite):
    def __init__(self):
        self.board = BOARD
        self.character = Character('assets/images/chars/placeholder.png', self.get_initial_player_position())
        self.wall_sprite = arcade.Sprite('assets/images/levels/wall.png')
        
       
        self.width = len(self.board[0])
        self.height = len(self.board)

    def get_sprite_position(self, r, c):
        x = c * BLOCK_SIZE + (BLOCK_SIZE // 2)
        y = r * BLOCK_SIZE + (BLOCK_SIZE + (BLOCK_SIZE // 2))
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
        self.character.draw()
        for r in range(self.height):
            for c in range(self.width):
                if self.is_wall_at((r,c)):
                    self.draw_sprite(self.wall_sprite, r, c)
        a, b = self.character.board_position
        # self.character.set_position(a+1, b)
        # self.character.draw()
        self.draw_sprite(self.character, a, b)

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

    def check_collision_and_move(self):
        offsets = [(0,1), (1,0), (-1,0), (0,-1)]
        for offset in offsets:
            check_pos = (self.character.board_position[0] + offset[0], self.character.board_position[1] + offset[1])
            if self.is_obstacle_char(check_pos):
                pass
            else:
                print('')
                line = list(self.board[self.character.board_position[0]])
                line[self.character.board_position[1]] = '-'
                self.board[self.character.board_position[0]] = ''.join(line)

                self.character.board_position = check_pos
               
                line = list(self.board[check_pos[0]])
                line[check_pos[1]] = 'X'
                self.board[check_pos[0]] = ''.join(line)
                


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
        


class Character():
    def __init__(self, sprite_name, pos):
        self.sprite = arcade.Sprite(sprite_name)
        self.board_position = pos
        self.sprite.set_position(50, 50)
        self.sprite.width = 50
        self.sprite.height = 50
        self.next_direction = None

    def auto_move(self):
        pass

    def check_in_place(self):
        pass

    def update(self):
        x, y = self.get_sprite_position(r, c)
        self.sprite.set_position(x, y)
        self.draw()

    def draw(self):
        self.sprite.draw()

    def set_position(self, x, y):
        self.sprite.set_position(x, y)