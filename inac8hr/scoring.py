from inac8hr.events import Event
from inac8hr.entities import PollingStaUnit


class ScoringEngine():
    def __init__(self):
        self.total_score = 0
        self.factor = 1
        self.increment = 1
        self.score_changed = Event(self)

    def add_score(self, score: int):
        self.total_score += score*self.factor

    def increment_score(self):
        self.total_score += self.increment*self.factor
        self.on_score_change()

    def decrement_score(self):
        self.total_score -= self.increment*self.factor
        self.on_score_change()

    def deduct_score(self, score: int):
        self.total_score -= score*self.factor
        self.on_score_change()

    def on_score_change(self, *args):
        self.score_changed()

    @property
    def total(self):
        return self.total_score
