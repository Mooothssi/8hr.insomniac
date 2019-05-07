from ..globals import *
from ..utils import LocationUtil
from .particles import Bullet
from . import SelectableUnit, Unit, AnimatedEntity
from .agents import AgentUnit
import time
import random


class DefenderUnit(SelectableUnit, AnimatedEntity):
    STATE_SHOOTING = 1
    STATE_SELECTED = 2
    T_SELECTED = 1
    NORMAL_RADIUS = 26.7 # 0.8
    PROXIMITY_THRESHOLD = 5

    def __init__(self, texture_list: list, initial_pos, 
                 scaling=1):
        super().__init__(texture_list, initial_pos, scaling)
        AnimatedEntity.__init__(self, texture_list, initial_pos, anim_sprite=self.sprite)
        self.bullets = []
        self.current_bullet = None
        self.damage = 10
        self.placement_cost = 10
        self.bulldoze_cost = 10
        self.agent_limit = 0
        self.coverage_radius = DefenderUnit.NORMAL_RADIUS
        self.initial_pos = initial_pos
        self._bullet_type = Bullet
        self.defender_state = self.S_IDLE
        self.cooldown_duration = 1.2
        self.last_activity = None

    @property
    def bullet(self):
        return self.bullets[0]

    def cooled_down(self):
        if self.last_activity is None:
            return False
        else:
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
        bullet = self.get_ready()
        for bullet in self.bullets:
            bullet.fired = True
            bullet.damage = self.damage
            bullet.to(target_pos)
        self.current_bullet = bullet

    def disarm(self):
        self.current_bullet = None

    def on_animated(self):
        if self.defender_state == self.STATE_SHOOTING:
            remove_list = []
            for bullet in self.bullets:
                bullet.play()
                if bullet.disarmed:
                    remove_list.append(bullet)
            for i in remove_list:
                self.bullets.remove(i)
        else:
            if self.is_animated():
                if not self.cooled_down():
                    AnimatedEntity.stop_animating(self)
                    self.change_state('idle')
                AnimatedEntity.clocked_update(self)

    def on_selection(self, selected):
        super().on_selection(selected)
        if selected:
            self.change_state("selected")
        else:
            self.change_state("idle")

    def inspect(self, enemy: AgentUnit):
        pass

    def deal_enemy(self, enemy: AgentUnit):
        if enemy.processed or self.cooled_down():
            return False
        return True


class CalculatorUnit(DefenderUnit):
    def __init__(self, initial_pos, scaling=1):
        super().__init__(["assets/images/chars/calculator.png"], initial_pos, scaling)
        self.cooldown_duration = 1.2
        self.damage = 5

    def deal_enemy(self, enemy: AgentUnit):
        if super().deal_enemy(enemy):
            self.last_activity = time.time()
            self.shoot(enemy.position)


class PaperShredderUnit(DefenderUnit):
    def __init__(self, initial_pos, scaling=1):
        super().__init__(["assets/images/chars/shredder_40px.png"], initial_pos, scaling)
        super().add_state_texture_from_filename("selected", "assets/images/chars/unavail.png")
        super().add_state_texture_from_filenames("animated", ["assets/images/chars/shredder_1.png",
                                                 "assets/images/chars/shredder_2.png",
                                                 "assets/images/chars/shredder_3.png",
                                                 "assets/images/chars/shredder_4.png"], True)
        self.cooldown_duration = 120

    def deal_enemy(self, enemy: AgentUnit):
        if super().deal_enemy(enemy):
            dx, dy = self.sprite.position[0] - enemy.sprite.position[0], self.sprite.position[1] - enemy.sprite.position[1]
            if 0 <= dx <= 5:
                dx = 0
            else:
                dx /= abs(dx)
            if 0 <= dy <= 5:
                dy = 0
            else:
                dy /= abs(dy)
            for key in DIR_OFFSETS:
                if DIR_OFFSETS[key] == (dy, dx):
                    switch_point = [self.board_position, key]
                    enemy.pending_switches = enemy.switches[:]
                    enemy.switches = [switch_point]
                    enemy.eaten = True
                    self.last_activity = time.time()
                    enemy.processed = True
                    self.change_state("animated")
                    self.start_animating()
