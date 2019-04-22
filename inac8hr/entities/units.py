from arcade.sprite import Sprite
from inac8hr.globals import *
from inac8hr.utils import LocationUtil
from inac8hr.particles import Bullet
from inac8hr.physics import CirclePhysicsEntity
from inac8hr.imports import ExtendedSpriteList
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
        self.set_sprite_texture(Unit.T_DEFAULT)
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
        # self.set_texture_from_state(value)  

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
        self.sprite.scale = GAME_PREFS.scaling
        for file_name in self.texture_files:
            self.sprite.append_texture(arcade.load_texture(file_name))

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

    def scale(self, scaling):
        # self.init_sprites()
        # self.set_sprite_texture(0)#self.state)
        r, c = self.board_position
        self.set_board_position(r, c)

    def set_texture_from_state(self, state_no):
        self.sprite.scale = GAME_PREFS.scaling
        self.set_sprite_texture(Unit.TEXTURE_STATEMAP[state_no])

    def set_sprite_texture(self, texture_no):
        print(GAME_PREFS.scaling)
        self.sprite.scale = GAME_PREFS.scaling
        self.sprite.set_texture(texture_no)


class SelectableUnit(Unit):
    def __init__(self, sprite_name, initial_pos, scaling=1):
        super().__init__(sprite_name, initial_pos, scaling)
        self.selected = False

    def on_selection(self, selected):
        self.selected = selected


class UnitListBase():
    def __init__(self):
        self.sprites = ExtendedSpriteList()

    def __iter__(self):
        self.n = 0
        return self
       
    def __len__(self):
        return len(self.units)
    
    def draw(self):
        self.sprites.draw()


class UnitList(UnitListBase):
    def __init__(self):
        super().__init__()
        self.units = []

    def append(self, item: Unit):
        self.units.append(item)
        self.sprites.append(item.sprite)

    def remove(self, item: Unit):
        self.units.remove(item)
        self.sprites.remove(item.sprite)

    def __next__(self):
        if self.n <= len(self.units)-1 and len(self.units) > 0:
            result = self.units[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration


class UnitKeyedList(UnitListBase):
    def __init__(self):
        super().__init__()
        self.units = {}

    def __getitem__(self, key):
        return self.units[key]

    def __setitem__(self, key, value):
        self.units[key] = value
        self.sprites.append(value.sprite)

    def remove(self, item: Unit):
        self.units.remove(item)
        self.sprites.remove(item.sprite)
    
    def values(self):
        return self.units.values()

    def __next__(self):
        lst = list(self.units.values())
        if self.n <= len(self.units)-1 and len(self.units) > 0:
            result = lst[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

