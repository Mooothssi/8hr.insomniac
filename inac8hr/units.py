from arcade.sprite import Sprite
from inac8hr.utils import LocationUtil

class Unit():
    def __init__(self, sprite_name, initial_pos, scaling=1):
        self.sprite = Sprite(sprite_name)
        self.board_position = initial_pos
        self.next_board_pos = (0,0)
        self.scaling = scaling
        sp_pos_x, sp_pos_y = LocationUtil.get_sprite_position(initial_pos[0], initial_pos[1])
        self.sprite.set_position(sp_pos_x, sp_pos_y)
        self.sprite.width = 50
        self.sprite.height = 50

    def draw(self):
        self.sprite.draw()

    def pause(self):
        pass

    def play(self):
        pass

class DefenderUnit(Unit):
    pass

class AgentUnit(Unit):
    pass