from arcade.sprite import Sprite
from inac8hr.globals import *
from inac8hr.utils import LocationUtil
from inac8hr.particles import Bullet
from inac8hr.entities import Unit, AnimatedEntity


class AgentUnit(Unit, AnimatedEntity):

    TEXTURE_CONST = 0.25
    DECAY_VARIANTS = 3

    def __init__(self, texture_list, pos, full_hp=50, scaling=1, switches=[]):
        super().__init__(texture_list, pos, scaling)
        self.decay_textures = []
        self.next_direction = DIR_STILL
        self.switches = list(switches)
        self.survived = False
        self.targeted = False
        self.time_lived = 0
        self.reset_hp(full_hp)

    @property
    def position(self):
        return self.sprite.position

    def change_direction(self, direction):
        self.next_direction = direction

    def reset_hp(self, hp):
        self.full_health = hp
        self.health = self.full_health

    def on_animated(self, *kwargs):
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
        self.dead = True
        self.survived = True

    def move(self):
        if self.check_if_overlapping():
            self.board_position = self.next_board_pos
            #reset_pos_x, reset_pos_y = LocationUtil.get_sprite_position(self.board_position[0], self.board_position[1])
        else:
            x, y = self.sprite.position[0], self.sprite.position[1]
            rand_velc = 2#(random.randint(1,50)/20)
            #self.set_position(x + DIR_OFFSETS[self.next_direction][1]*rand_velc, y + DIR_OFFSETS[self.next_direction][0]*rand_velc)
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
    pass


class JumpedBallot(Ballot):
    pass
