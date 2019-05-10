import arcade
from inac8hr.globals import GAME_PREFS
from inac8hr.levels.base import Level
from inac8hr.cycles import CycleClock
from inac8hr.scoring import ScoringEngine
from inac8hr.tuning import ScoringFactor
from inac8hr.entities import UnitList, UnitKeyedList, PollingStaUnit, Ballot


class LV1Scoring(ScoringEngine):
    def __init__(self):
        from inac8hr.engines import AudioEngine

        super().__init__()
        self.voter_count = 0
        self.turnout = 0
        self.budget = 0
        self.jumped = True
        self.jumped_count = 0
        self.valid_count = 0
        self.jumping_limit = 580
        self.cycle_number = 1
        self.mode_factor = ScoringFactor.HARD_FACTOR
        self.velocity_factors = (ScoringFactor.FIRST_STAGE_FACTOR, ScoringFactor.SECOND_STAGE_FACTOR, ScoringFactor.THIRD_STAGE_FACTOR, ScoringFactor.FOURTH_STAGE_FACTOR)
        self.phases = CycleClock.DEFAULT_CYCLES_LIMIT // len(self.velocity_factors)
        self.audio = AudioEngine.get_instance()

    def recount_ballot(self, generators: list):
        missing_valid_count = self.voter_count - self.valid_count
        self.total_score -= missing_valid_count
        self.on_score_change()
        self.jumped_count = 0
        self.valid_count = 0
        # for g in generators:
        #     self.voter_count += g.ballots

    def add_ballot_from_generator(self, g, *args):
        result = (self.cycle_number % 2) + (self.cycle_number // 2) - 1
        g.ballot_velocity = self.velocity_factors[result]
        self.voter_count += g.ballots
        self.on_score_change()

    def increment_score(self):
        super().increment_score()

    def decrement_score(self):
        super().decrement_score()

    def update_ballot(self, valid):
        if valid:
            self.valid_count += 1
            self.total_score += 1*self.mode_factor
        else:
            self.jumped_count += 1
            self.total_score -= 1
            self.audio.play_by_id("AGENTS/BALLOT_SPOILT_COUNTED")
        self.on_score_change()

    def increment_turnout(self):
        self.turnout += 1

    def decrement_turnout(self):
        self.turnout -= 1

    def adjust_velocity(self, units, cycle_number):
        self.cycle_number = cycle_number
        result = (cycle_number % 2) + (cycle_number // 2) - 1
        for unit in units:
            unit.velocity = self.velocity_factors[result]

    def on_score_change(self, *args):
        self.jumped = self.turnout > self.voter_count
        super().on_score_change(args)


class LV1Level(Level):
    def __init__(self):
        self.generators = UnitKeyedList()
        super().__init__()
        self.scoring = LV1Scoring()
        self.cycle.cycle_changed += self.on_cycle_changed
        for i in self.map_plan.get_all_generators():
            self.generators[i.initial_pos] = i
            i.generate(self)
            i.gen_cycle_ended += self.scoring.add_ballot_from_generator
        self.scoring.recount_ballot(self.generators)
        self.death = 0

    def register_graphics(self):
        super().register_graphics()
        # self.add_drawable_child(self.generators)

    def draw(self):
        super().draw()
        self.generators.draw()

    def play(self):
        super().play()
        for g in self.generators.values():
            g.play()

    def on_resize(self):
        self.generators.scale(GAME_PREFS.scaling)
        if self.scaling != GAME_PREFS.scaling:
            self.generators.displace_by_screen_res(GAME_PREFS.screen_width, GAME_PREFS.screen_height)
            self.enemies.displace_by_screen_res(GAME_PREFS.screen_width, GAME_PREFS.screen_height)
        super().on_resize()

    def on_cycle_changed(self, sender, *args):
        for g in self.generators:
            g.generate(self)
        self.scoring.adjust_velocity(self.enemies, sender.current_cycle)
        self.scoring.recount_ballot(self.generators)

    def calculate_the_dead(self, enemy: Ballot):
        if enemy.jumped:
            if enemy.survived:
                self.scoring.increment_turnout()
                self.scoring.update_ballot(False)
        else:
            if enemy.survived:
                self.scoring.increment_turnout()
                self.scoring.update_ballot(True)
        self.enemies.remove(enemy)
