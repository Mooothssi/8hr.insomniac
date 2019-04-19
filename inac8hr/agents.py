import arcade
from inac8hr.imports import *

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

class Character():
    def __init__(self, sprite_name, pos, scaling=1):
        self.sprite = PreferredSprite(sprite_name)
        self.board_position = pos
        self.next_board_pos = (0,0)
        self.scaling = scaling
        sp_pos_x, sp_pos_y = self.get_sprite_position(pos[0], pos[1])
        self.sprite.set_position(sp_pos_x, sp_pos_y)
        self.sprite.width = 50
        self.sprite.height = 50
        self.next_direction = DIR_UP
        #print(pos)

    def check_if_overlapping(self):
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
        #print(self.next_direction)
      
        self.next_direction = direction

    def move(self):
        if self.check_if_overlapping():
            self.board_position = self.next_board_pos
            reset_pos_x, reset_pos_y = self.get_sprite_position(self.board_position[0],self.board_position[1])
            #self.set_position(reset_pos_x, reset_pos_y)
        else:
            x, y = self.sprite.position[0], self.sprite.position[1]#self.get_sprite_position(self.board_position[0], self.board_position[1])
            rand_velc = 2 #(random.randint(1,20)/20)
            self.set_position(x + DIR_OFFSETS[self.next_direction][1]*rand_velc, y + DIR_OFFSETS[self.next_direction][0]*rand_velc)
        #print(f'Curr pos: {self.sprite.position}')

    def update(self):
        self.move()
        #self.draw()

    def draw(self):
        self.sprite.draw()

    def set_position(self, x, y):
        self.sprite._position = [x,y]