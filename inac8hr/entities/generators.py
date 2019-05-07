from ..entities import SelectableUnit, Unit, AgentUnit, Ballot
from ..globals import GAME_PREFS
from ..events import Event
import time
import random 


class PollingStaUnit(SelectableUnit):
    DEFAULT_PER_CYCLE = 25

    def __init__(self, texture_list: list, initial_pos, directions=[], scaling=1):
        super().__init__(texture_list, initial_pos, scaling)
        self.generation_factor = 1
        self.jumped_ballot_full_health = 10
        self.ballot_velocity = 1
        self.initial_pos = initial_pos
        self.jumped_ballots = 0
        self.ballots = 0
        self.directions = directions
        self.agents_per_cycle = PollingStaUnit.DEFAULT_PER_CYCLE
        self.agent = None
        self.generation_period = 0.75
        self.generation_start = time.time()
        self.gen_cycle_ended = Event(self)
        self.__generating__ = False
        self._level = None
        self._generate_this_time = 0

    @property
    def period_ended(self):
        return time.time() - self.generation_start >= self.generation_period

    def generate(self, level):
        self.__generating__ = True
        self._level = level
        self.jumped_ballots = 0
        self.ballots = 0
        # diff = 0
        # self.ballots = 0
        # for _ in range(self.agents_per_cycle):
        #     files = ['Ballot_pink.png', 'Ballot_orange.png', 'Ballot_red.png']
        #     r = random.randint(0, len(files)-1)
        #     jumped = bool(random.randint(0, 1))
        #     enemy = Ballot([f'assets/images/chars/{files[r]}'], self.initial_pos, 
        #                        self.jumped_ballot_full_health, 1,
        #                        self.directions, jumped)
        #     if jumped:
        #         self.jumped_ballots += 1
        #     else:
        #         self.ballots += 1
        #     enemy.displace_position(0, diff)
        #     diff += 40
        #     level.enemies.append(enemy)
        # self.jumped_ballot_full_health += 10

    def generate_one(self):
        if self._level is not None:
            files = ['Ballot_pink.png', 'Ballot_orange.png', 'Ballot_red.png']
            r = random.randint(0, len(files)-1)
            jumped = bool(random.randint(0, 1))
            enemy = Ballot([f'assets/images/chars/{files[r]}'], self.initial_pos, 
                                self.jumped_ballot_full_health, 1,
                                self.directions, jumped)
            enemy.velocity = self.ballot_velocity
            if jumped:
                self.jumped_ballots += 1
            else:
                self.ballots += 1
            self._generate_this_time += 1
            self._level.enemies.append(enemy)

    def play(self):
        super().play()
        if self.__generating__:
            if self.period_ended:
                self.generate_one()
                self.generation_start = time.time()
                if self._generate_this_time >= self.agents_per_cycle:
                    self.__generating__ = False
                    self.gen_cycle_ended()
                    self._generate_this_time = 0

    @property
    def total_ballots(self):
        return self.ballots + self.jumped_ballots

    def reset_to_full_health(self, unit, level):
        unit.reset_hp(unit.full_health * level.scoring.factor)


class SetPieceUnit():
    pass
