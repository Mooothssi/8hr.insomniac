from arcade.sprite import Sprite
from ..globals import *
from ..utils import LocationUtil
from .particles import Bullet
from . import Unit, AnimatedEntity


class AgentUnit(Unit, AnimatedEntity):

    TEXTURE_CONST = 0.25
    DECAY_VARIANTS = 3

    def __init__(self, texture_list, pos, full_hp=50, scaling=1, switches=[]):
        super().__init__(texture_list, pos, scaling)
        AnimatedEntity.__init__(self, texture_list, pos, anim_sprite=self.sprite)
        self.decay_textures = []
        self.velocity = 1
        self.next_direction = DIR_STILL
        self.switches = list(switches)
        self.survived = False
        self.targeted = False
        self.time_lived = 0
        self.reset_hp(full_hp)
        self.start_animating()

    @property
    def position(self):
        return self.sprite.position

    def change_direction(self, direction):
        self.next_direction = direction

    def reset_hp(self, hp):
        self.full_health = hp
        self.health = self.full_health

    def on_animated(self, *kwargs):
        AnimatedEntity.clocked_update(self)
        self.move_along_switches(self.switches)
        result = (self.health/self.full_health)*self.DECAY_VARIANTS
        if result < 1:
            result = 1
        else:
            result = round(result, 0)
        self.sprite.scale = (result)*self.TEXTURE_CONST

    def take_damage(self, hp):
        self.health -= hp
        if self.health <= 0:
            self.dead = True
    
    def won(self):
        # self.dead = True
        self.survived = True

    def move(self):
        if self.check_if_overlapping():
            self.board_position = self.next_board_pos
        else:
            x, y = self.sprite.position[0], self.sprite.position[1]
            rand_velc = self.velocity
            self.sprite.change_x = DIR_OFFSETS[self.next_direction][1]*rand_velc
            self.sprite.change_y = DIR_OFFSETS[self.next_direction][0]*rand_velc
            self.sprite.update()

    def move_along_switches(self, switch_points):
        if len(switch_points) == 0:
            self.won()
            return
        check_pos, offset_key = switch_points[0][0], switch_points[0][1]
        self.next_board_pos = check_pos
        self.change_direction(offset_key)
        if self.check_if_overlapping():
            switch_points.pop(0)
        self.move()

    def check_if_overlapping(self):
        r, c = self.next_board_pos
        next_x, next_y = LocationUtil.get_sprite_position(r, c)
        curr_x, curr_y = self.sprite.position
        return (curr_x - next_x)*DIR_OFFSETS[self.next_direction][1] >= 0 and (curr_y - next_y)*DIR_OFFSETS[self.next_direction][0] >= 0


class Ballot(AgentUnit):
    def __init__(self, texture_list, pos, full_hp=50,
                 scaling=1, switches=[], jumped=False):
        super().__init__(texture_list, pos, full_hp, scaling, switches)
        self.jumped = jumped
        self.overlay_sprite = Sprite("assets/images/chars/ballot_drop_masked.png")
        self._overlay_shown = False
        self._overlay_flag = False
        r, c = self.switches[-1][0]
        self.exit_point = r + 1, c
        self._anim_end = False
        self.sprite_list.insert(0, self.overlay_sprite)

    def _show_overlay(self):
        self.overlay_sprite.set_position(int(self.sprite.position[0]), int(self.sprite.position[1] - 7))
        self._overlay_shown = True

    def _move_ballot_anim(self):
        r, c = self.exit_point
        x, y = LocationUtil.get_sprite_position(r, c)
        if self.sprite.position[1] < self.sprite.position[1] + 200 and self.sprite.angle < 45:
            self.sprite.set_position(self.sprite.position[0], self.sprite.position[1] + 1)
            self.sprite.angle += 1
        else:
            # self._show_overlay()
            self.z_order_changed(self.sprite_list)
            if not self._anim_end:
                self.switches.append([self.exit_point, 3])
                self._anim_end = True

    def draw(self):
        pass
        # if self._overlay_shown:
        #     self.overlay_sprite.draw()

    def won(self):
        super().won()
        if self.survived and not self._overlay_flag:
            self.switches.append([self.exit_point, 1])
            self._overlay_flag = True

    def on_animated(self, *args):
        super().on_animated(*args)
        if self._overlay_flag:
            if len(self.switches) == 0 and not self._overlay_shown:
                self._show_overlay()
            elif self._overlay_shown:
                self._move_ballot_anim()
                if len(self.switches) == 0 and self._anim_end:
                    self.dead = True
                    self._overlay_shown = False

    def goto_box(self, box_loc):
        pass

