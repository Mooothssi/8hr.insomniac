from arcade.sprite import Sprite
from inac8hr.globals import *
from inac8hr.utils import LocationUtil
from inac8hr.particles import Bullet
from inac8hr.physics import CirclePhysicsEntity
import time
import random


class Unit(CirclePhysicsEntity):
    S_IDLE = 0
    S_ANIMATED = 1
    T_DEFAULT = 0
    TEXTURE_STATEMAP = {
        S_IDLE: T_DEFAULT,
        S_ANIMATED: T_DEFAULT
    }

    def __init__(self, texture_files: list, initial_pos, scaling=1):
        x, y = LocationUtil.get_sprite_position(*initial_pos)
        # TODO: Absolute and Relative position
        # self.sprite = Sprite()
        self.texture_files = texture_files
        # for file_name in texture_files:
        #     self.sprite.append_texture(arcade.load_texture(file_name))
        #     print(file_name)
        self.scaling = scaling
        self.init_sprites()
        self.board_position = 0, 0 
        r, c = initial_pos
        self.set_board_position(r, c)
        self.next_board_pos = (0, 0)
        
        self.sprite.width = 50
        self.sprite.height = 50
        self.curr_texture = None
        self.state = Unit.S_ANIMATED
        self.dead = False
        super().__init__([x, y], 25)

    def get_x1(self):
        return self.sprite.position[0]

    def set_x1(self, value):
        self.sprite.center_x = value

    def get_y1(self):
        return self.sprite.position[1]

    def set_y1(self, value):
        self.sprite.center_y = value

    def get_state(self):
        return self.__state__

    def set_state(self, value):
        self.__state__ = value
        self.set_sprite_texture(value)  

    def get_sprite(self):
        return self._sprite

    def set_sprite(self, value):
        self._sprite = value

    x1 = property(get_x1, set_x1)
    y1 = property(get_y1, set_y1)
    state = property(get_state, set_state)
    sprite = property(get_sprite, set_sprite)

    def draw(self):
        self.sprite.draw()

    def init_sprites(self):
        self.sprite = Sprite()
        for file_name in self.texture_files:
            self.sprite.append_texture(arcade.load_texture(file_name))

    def scale(self, scaling):
        self.scaling = GAME_PREFS.scaling
        self.init_sprites()
        self.set_sprite_texture(self.state)
        r, c = self.board_position
        self.set_board_position(r, c)

    def set_board_position(self, r, c):
        self.board_position = r, c
        sp_pos_x, sp_pos_y = LocationUtil.get_sprite_position(r, c)
        self.sprite.set_position(sp_pos_x, sp_pos_y)

    def set_position(self, x, y):
        self.sprite.set_position(x, y)

    def displace_position(self, x, y):
        self.sprite.set_position(self.sprite.center_x + x,
                                 self.sprite.center_y + y)

    def clocked_update(self):
        pass

    def die(self):
        self.dead = True

    def pause(self):
        self.state = Unit.S_IDLE

    def play(self):
        self.state = Unit.S_ANIMATED
        self.on_animated()

    def on_animated(self):
        pass

    def set_sprite_texture(self, texture_no):
        tex = Unit.TEXTURE_STATEMAP[texture_no]
        self.sprite.scale = GAME_PREFS.scaling
        self.sprite.set_texture(tex)


class SelectableUnit(Unit):
    def __init__(self, sprite_name, initial_pos, scaling=1):
        super().__init__(sprite_name, initial_pos, scaling=1)
        self.selected = False

    def on_selection(self):
        self.selected = True