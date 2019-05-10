from ..graphics import Sprite, DrawableLayer
from inac8hr.globals import *
from ..events import Event
from inac8hr.utils import LocationUtil
from .particles import Bullet
from inac8hr.physics import CirclePhysicsEntity
from inac8hr.imports import ExtendedSpriteList
import time
from inac8hr.utils import LocationUtil
import random


class Unit(CirclePhysicsEntity):
    S_IDLE = 0
    S_ANIMATED = 1
    T_DEFAULT = 0
    TEXTURE_STATEMAP = {
        S_IDLE: T_DEFAULT,
        S_ANIMATED: T_DEFAULT
    }

    def __init__(self, texture_files: list, initial_pos, scaling=1, initial_state="idle"):
        x, y = LocationUtil.get_sprite_position(*initial_pos)
        # TODO: Absolute and Relative position
        self.texture_state = initial_state
        self.texture_groups = {}
        self.texture_files = texture_files



        self.scaling = scaling
        self.init_sprites()
        self.board_position = 0, 0 
        r, c = initial_pos
        self.set_board_position(r, c)
        self.next_board_pos = (0, 0)     
        self.sprite.width = 50
        self.sprite.height = 50
        self._current_texture_group = None
        self.state = Unit.S_ANIMATED
        self.set_sprite_texture(Unit.T_DEFAULT)
        self.dead = False
        self.z_order_changed = Event(self)
        self.sprite_list = []
        self.sprite_list.append(self.sprite)
        super().__init__([x, y], 25)

#
# Getters, setters, and properties
#

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

    def get_sprite(self):
        return self._sprite

    def set_sprite(self, value):
        self._sprite = value

    x1 = property(get_x1, set_x1)
    y1 = property(get_y1, set_y1)
    state = property(get_state, set_state)
    sprite = property(get_sprite, set_sprite)
#
#
#

    def draw(self):
        self.sprite.draw()

    def add_state_texture_from_filename(self, tex_class, filename: str, animated=False):
        if tex_class not in self.texture_groups:
            tex_group = EntityTextureGroup(tex_class)
            tex_group.animated = animated
            tex_group.add_texture_from_filename(filename, GAME_PREFS.scaling)
            self.texture_groups[tex_class] = tex_group
        else:
            tex_group = self.texture_groups[tex_class]
            tex_group.add_texture_from_filename(filename, GAME_PREFS.scaling)

    def add_state_texture_from_filenames(self, tex_class, filenames: list, animated=False):
        for filename in filenames:
            self.add_state_texture_from_filename(tex_class, filename, animated)

    def apply_textures(self, tex_class):
        self.sprite.textures.clear()
        for texture in self.texture_groups[tex_class]:
            self.sprite.append_texture(texture)
        self.sprite.set_texture(0)
        self._current_texture_group = self.texture_groups[tex_class]

    def init_sprites(self):
        self.sprite = Sprite()
        self.sprite.scale = GAME_PREFS.scaling
        self.add_state_texture_from_filenames(self.texture_state, self.texture_files)
        self.apply_textures(self.texture_state)
        self.sprite.scale = GAME_PREFS.scaling

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
        self.sprite.scale = GAME_PREFS.scaling
        r, c = self.board_position
        self.set_board_position(r, c)

    def change_state(self, state):
        self.sprite.scale = GAME_PREFS.scaling
        self.apply_textures(state)

    # def set_texture_from_state(self, state_no):
    #     self.sprite.scale = GAME_PREFS.scaling
    #     self.set_sprite_texture(Unit.TEXTURE_STATEMAP[state_no])

    def set_sprite_texture(self, texture_no):
        self.sprite.scale = GAME_PREFS.scaling
        self.sprite.set_texture(texture_no)

    def is_animated(self):
        if self._current_texture_group is None:
            return False
        else:
            return self._current_texture_group.animated


class SelectableUnit(Unit):
    def __init__(self, sprite_name, initial_pos, scaling=1):
        super().__init__(sprite_name, initial_pos, scaling)
        self.selected = False

    def on_selection(self, selected):
        self.selected = selected


class EntityTextureGroup():
    def __init__(self, texture_class: str, animated=False):
        self.texture_class = texture_class
        self.textures = []
        self.animated = animated

    def add_texture_from_filename(self, filename, scaling=1):
        tex = arcade.load_texture(filename, scale=scaling)
        self.textures.append(tex)

    def scale(self, scaling_factor=1):
        for tex in self.textures:
            tex.scale = scaling_factor

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n <= len(self.textures)-1 and len(self.textures) > 0:
            result = self.textures[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration


class AnimatedEntity():
    def __init__(self, animations_tex, initial_pos, scaling=1, anim_sprite:Sprite=None):
        self.frame_time = 0.75
        self.curr_time = 0
        self.passed_frames = 0
        # if anim_sprite is not None:
        self.animated_sprite = anim_sprite
        # else:
        #     self.animated_sprite = Sprite()
        #     for tex in animations_tex:
        #         self.animated_sprite.append_texture(tex)
        self.animated_textures = animations_tex
        # self.texture_frames = len(self.animated_textures)
        self.__animating__ = False

    def start_animating(self):
        self.curr_time = time.time()
        self.__animating__ = True

    def stop_animating(self):
        self.__animating__ = False

    def clocked_update(self):
        if self.texture_frames <= 1:
            return
        elapsed = time.time() - self.curr_time
        if elapsed >= self.frame_time:
            r = self.passed_frames % self.texture_frames
            self.animated_sprite.set_texture(r)
            self.passed_frames += 1
            self.curr_time = time.time()

    @property
    def texture_frames(self):
        return len(self.animated_sprite.textures)
    # def draw(self):
    #     if self.__animating__:
    #         self.animated_sprite.draw()
    #     else:
    #         self.sprite.draw()


class UnitListBase():
    def __init__(self):
        self.screen_res = GAME_PREFS.screen_width, GAME_PREFS.screen_height
        self.sprites = ExtendedSpriteList()
        self.layer = DrawableLayer()
        self.scaling_factor = 1

    def __iter__(self):
        self.n = 0
        return self

    def __len__(self):
        return len(self.units)

    def draw(self):
        self.sprites.draw()
        # self.layer.draw()

    def scale(self, scaling_factor):
        self.scaling_factor = scaling_factor
        for sprite in self.sprites.sprite_list:
            sprite.scale = scaling_factor

    def displace_by_screen_res(self, width, height):
        for sprite in self.sprites.sprite_list:
            r, c = LocationUtil.get_plan_position(sprite.position[0], sprite.position[1], False, True)
            x, y = LocationUtil.get_sprite_position(r, c)
            sprite.set_position(x, y)

    def on_item_added(self, item):
        item.z_order_changed += self.on_z_order_changed

    def on_item_removed(self, item):
        item.z_order_changed -= self.on_z_order_changed

    def on_z_order_changed(self, sender, *args):
        pass


class UnitList(UnitListBase):
    def __init__(self):
        super().__init__()
        self.units = []

    def append(self, item: Unit):
        self.units.append(item)
        item.sprite.scale = self.scaling_factor
        for sprite in item.sprite_list:
            self.sprites.append(sprite)
            # self.layer.queue(sprite)
        self.on_item_added(item)

    def remove(self, item: Unit):
        self.units.remove(item)
        for sprite in item.sprite_list:
            self.sprites.remove(sprite)
            # self.layer.remove(sprite)
        self.on_item_removed(item)

    def __next__(self):
        if self.n <= len(self.units)-1 and len(self.units) > 0:
            result = self.units[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration


class UnitKeyedList(UnitListBase):
    """
        Serves as a simple spatial hash for each unit
    """
    def __init__(self):
        super().__init__()
        self.units = {}

    def __getitem__(self, key):
        return self.units[key]

    def __setitem__(self, key, value: Unit):
        self.units[key] = value
        value.sprite.scale = self.scaling_factor
        self.on_item_added(value)
        for sprite in value.sprite_list:
            self.sprites.append(sprite)
            # self.layer.queue(sprite)

    def remove(self, item: Unit):
        self.on_item_removed(item)
        self.units.remove(item)
        self.sprites.remove(item.sprite)
        # self.layer.remove(item.sprite)

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
