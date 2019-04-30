from inac8hr.globals import *
from inac8hr.levels.base import Level
from inac8hr.cycles import CycleClock
from inac8hr.scoring import ScoringEngine
from inac8hr.tuning import ScoringFactor
from inac8hr.entities import UnitList, UnitKeyedList, GeneratorUnit


class LV1Scoring(ScoringEngine):
    def __init__(self):
        super().__init__()
        self.voter_count = ScoringFactor.LV1_DEFAULT_BALLOT
        self.turnout = ScoringFactor.LV1_DEFAULT_BALLOT
        self.jumped = True
        self.jumping_limit = 580

    def increment_score(self):
        super().increment_score()
        self.turnout -= 1

    def decrement_score(self):
        super().decrement_score()
        self.turnout += 1

    def on_score_change(self, *args):
        self.jumped = self.turnout > self.voter_count
        super().on_score_change(args)


class LV1Level(Level):
    def __init__(self):
        super().__init__()
        self.scoring = LV1Scoring()
        self.generators = UnitKeyedList()
        for i in self.map_plan.get_all_generators():
            self.generators[i.initial_pos] = i

    def draw(self):
        super().draw()
        self.generators.draw()

    def on_resize(self):
        super().on_resize()
        self.generators.scale(GAME_PREFS.scaling)

