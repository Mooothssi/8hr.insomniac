from ..globals import *
from ..utils import LocationUtil
from .particles import Bullet
from . import SelectableUnit, Unit
import time
import random


class DefenderUnit(SelectableUnit):
    STATE_SHOOTING = 1
    STATE_SELECTED = 2
    T_SELECTED = 1
    NORMAL_RADIUS = 26.7#0.8

    def __init__(self, texture_list: list, initial_pos, scaling=1):
        super().__init__(texture_list, initial_pos, scaling)
        self.bullets = []
        self.coverage_radius = DefenderUnit.NORMAL_RADIUS
        self.initial_pos = initial_pos
        self.defender_state = self.S_IDLE
        self.target_pos = (-1, -1)
        self.cooldown_duration = 1.2
        self.last_activity = time.time()

    @property
    def bullet(self):
        return self.bullets[0]

    def cooled_down(self):
        return time.time() - self.last_activity <= self.cooldown_duration

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
        if not self.cooled_down():
            bullet = self.get_ready()
            for bullet in self.bullets:
                bullet.fired = True
                bullet.to(self.target_pos)
            self.last_activity = time.time()
            return bullet

    def on_animated(self):
        if self.defender_state == self.STATE_SHOOTING:
            remove_list = []
            for bullet in self.bullets:
                bullet.play()
                if bullet.disarmed:
                    remove_list.append(bullet)
            for i in remove_list:
                self.bullets.remove(i)

    def on_selection(self, selected):
        super().on_selection(selected)
        if selected:
            self.set_sprite_texture(self.T_SELECTED)
        else:
            self.set_sprite_texture(Unit.T_DEFAULT)


class CalculatorUnit(DefenderUnit):
    pass
