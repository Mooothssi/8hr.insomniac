from inac8hr.globals import *
from inac8hr.levels.base import Level
from inac8hr.cycles import CycleClock
from inac8hr.scoring import ScoringEngine
from inac8hr.tuning import ScoringFactor
from inac8hr.entities import UnitList, UnitKeyedList, PollingStaUnit, Ballot


class LV1Scoring(ScoringEngine):
    def __init__(self):
        super().__init__()
        self.voter_count = ScoringFactor.LV1_DEFAULT_BALLOT
        self.turnout = ScoringFactor.LV1_DEFAULT_BALLOT
        self.jumped = True
        self.jumping_limit = 580

    def recount_ballot(self, generators: list):
        self.voter_count = 0
        self.turnout = 0
        for g in generators:
            self.voter_count += g.ballots
            self.turnout += g.total_ballots

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
        self.cycle.cycle_changed += self.on_cycle_changed
        for i in self.map_plan.get_all_generators():
            self.generators[i.initial_pos] = i
            i.generate(self)
        self.scoring.recount_ballot(self.generators)

    def draw(self):
        super().draw()
        self.generators.draw()

    def on_resize(self):
        super().on_resize()
        self.generators.scale(GAME_PREFS.scaling)
        self.generators.displace_by_screen_res(GAME_PREFS.screen_width, GAME_PREFS.screen_height)
        self.enemies.displace_by_screen_res(GAME_PREFS.screen_width, GAME_PREFS.screen_height)

    def on_cycle_changed(self, sender, *args):
        # self.generate_enemies()
        for g in self.generators:
            g.generate(self)
        self.scoring.recount_ballot(self.generators)

    def calculate_the_dead(self, enemy: Ballot):
        if enemy.jumped:
            if enemy.survived:
                self.scoring.decrement_score()
            else:
                self.scoring.increment_score()
        else:
            if enemy.survived:
                self.scoring.increment_score()
            else:
                self.scoring.decrement_score()
        self.enemies.remove(enemy)