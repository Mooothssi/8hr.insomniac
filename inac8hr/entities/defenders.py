from ..globals import *
from ..utils import LocationUtil
from .particles import Bullet
from . import SelectableUnit, Unit
from .agents import AgentUnit
import time
import random


class DefenderUnit(SelectableUnit):
    STATE_SHOOTING = 1
    STATE_SELECTED = 2
    T_SELECTED = 1
    NORMAL_RADIUS = 26.7#0.8

    def __init__(self, texture_list: list, initial_pos, 
                 scaling=1):
        super().__init__(texture_list, initial_pos, scaling)
        self.bullets = []
        self.damage = 10
        self.agent_limit = 0
        self.coverage_radius = DefenderUnit.NORMAL_RADIUS
        self.initial_pos = initial_pos
        self._bullet_type = Bullet
        self.defender_state = self.S_IDLE
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
        bullet = self._bullet_type('assets/images/particle.png', self.initial_pos)
        bullet.damage = self.damage
        self.bullets.append(bullet)
        self.defender_state = self.STATE_SHOOTING
        return self.bullet

    def shoot(self, target_pos):
        if not self.cooled_down():
            bullet = self.get_ready()
            for bullet in self.bullets:
                bullet.fired = True
                bullet.to(target_pos)
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

    def inspect(self, enemy: AgentUnit):
        pass


class CalculatorUnit(DefenderUnit):
    def __init__(self, initial_pos, scaling=1):
        super().__init__(["assets/images/chars/calculator.png"], initial_pos, scaling)
        self.damage = 50


class PaperShredderUnit(DefenderUnit):
    def __init__(self, initial_pos, scaling=1):
        super().__init__(["assets/images/chars/shredder_40px.png", "assets/images/chars/unavail.png"], initial_pos, scaling)
