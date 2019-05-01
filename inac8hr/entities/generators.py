from inac8hr.entities import SelectableUnit, Unit, AgentUnit, Ballot
from inac8hr.globals import GAME_PREFS
import random 


class PollingStaUnit(SelectableUnit):
    DEFAULT_PER_CYCLE = 25

    def __init__(self, texture_list: list, initial_pos, scaling=1):
        super().__init__(texture_list, initial_pos, scaling)
        self.generation_factor = 1
        self.jumped_ballot_full_health = 10
        self.initial_pos = initial_pos
        self.jumped_ballots = 0
        self.ballots = 0
        self.agents_per_cycle = PollingStaUnit.DEFAULT_PER_CYCLE
        self.agent = None

    def generate(self, level):
        diff = 0
        for _ in range(self.agents_per_cycle):
            files = ['Ballot_pink.png', 'Ballot_orange.png', 'Ballot_red.png']
            jumped = bool(random.randint(0, 1))
            enemy = Ballot([f'assets/images/chars/{files[0]}'], self.initial_pos, 
                               self.jumped_ballot_full_health, 1,
                               level.map_plan.ballot_switch_points, jumped)
            if jumped:
                self.jumped_ballots += 1
            else:
                self.ballots += 1
            enemy.displace_position(0, diff)
            diff += 40
            level.enemies.append(enemy)
        self.jumped_ballot_full_health += 10
    
    @property
    def total_ballots(self):
        return self.ballots + self.jumped_ballots

    def reset_to_full_health(self, unit, level):
        unit.reset_hp(unit.full_health * level.scoring.factor)


class SetPieceUnit():
    pass