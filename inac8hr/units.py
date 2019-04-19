from arcade.sprite import Sprite
from inac8hr.utils import LocationUtil

class Unit():
    def __init__(self, sprite_name, initial_pos, scaling=1):
        self.sprite_name = sprite_name
        self.sprite = Sprite(sprite_name)
        self.board_position = 0,0 
        r, c = initial_pos
        self.set_board_position(r, c)
        self.next_board_pos = (0,0)
        self.scaling = scaling
        self.sprite.width = 50
        self.sprite.height = 50

    def draw(self):
        self.sprite.draw()

    def scale(self, scaling):
        self.sprite = Sprite(self.sprite_name, scale=scaling)
        r, c = self.board_position
        self.set_board_position(r, c)

    def set_board_position(self, r, c):
        self.board_position = r, c
        sp_pos_x, sp_pos_y = LocationUtil.get_sprite_position(r, c)
        self.sprite.set_position(sp_pos_x, sp_pos_y)

    def pause(self):
        pass

    def play(self):
        pass

class DefenderUnit(Unit):
    pass

class AgentUnit(Unit):
    pass