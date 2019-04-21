from arcade.sprite import Sprite
from inac8hr.globals import *
from inac8hr.utils import LocationUtil
from inac8hr.particles import Bullet
from inac8hr.physics import CirclePhysicsEntity
import random


class Unit(CirclePhysicsEntity):
    def __init__(self, sprite_name, initial_pos, scaling=1):
        x, y = LocationUtil.get_sprite_position(*initial_pos)
        # TODO: Absolute and Relative position
        self.sprite_name = sprite_name
        self.sprite = Sprite(sprite_name)
        self.board_position = 0, 0 
        r, c = initial_pos
        self.set_board_position(r, c)
        self.next_board_pos = (0, 0)
        self.scaling = scaling
        self.sprite.width = 50
        self.sprite.height = 50
        self.state = UNIT_ANIMATED
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
    
    x1 = property(get_x1, set_x1)
    y1 = property(get_y1, set_y1)

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
        self.state = UNIT_FROZEN

    def play(self):
        self.state = UNIT_ANIMATED
        self.on_animated()

    def on_animated(self):
        pass


class DefenderUnit(Unit):
    STATE_IDLE = 0
    STATE_SHOOTING = 1

    def __init__(self, sprite_name, initial_pos, scaling=1):
        super().__init__(sprite_name, initial_pos, scaling)
        self.bullets = []
        self.initial_pos = initial_pos
        self.defender_state = self.STATE_IDLE
        self.target_pos = (-1, -1)

    @property
    def bullet(self):
        return self.bullets[0]

    def draw(self):
        super().draw()
        for bullet in self.bullets:
            if bullet.fired:
                bullet.draw()

    def get_ready(self):
        bullet = Bullet('assets/images/particle.png', self.initial_pos)
        self.bullets.append(bullet) 
        self.defender_state = self.STATE_SHOOTING
        return bullet

    def shoot(self):
        for bullet in self.bullets:
            bullet.fired = True
            bullet.to(self.target_pos)  

    def on_animated(self):
        if self.defender_state == self.STATE_SHOOTING:
            remove_list = []
            for bullet in self.bullets:
                bullet.play()
                if bullet.disarmed:
                    remove_list.append(bullet)
            for i in remove_list:
                self.bullets.remove(i)


class AgentUnit(Unit):
    def __init__(self, sprite_name, pos, scaling=1, switches=[]):
        super().__init__(sprite_name, pos, scaling)
        self.next_direction = DIR_STILL
        self.switches = list(switches)
        self.survived = False
        self.targeted = False

    @property
    def position(self):
        return self.sprite.position

    def change_direction(self, direction):
        self.next_direction = direction

    def on_animated(self, *kwargs):
        self.move_along_switches(self.switches)
    
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