from inac8hr.layers import PlayableSceneLayer

LV_PLAYING = 1
LV_PAUSED = 0

class Level(PlayableSceneLayer):
    def __init__(self):
        self.map_plan = None
        self.defenders = []
        self.enemies = []
        self.state = LV_PAUSED

    #
    # Arcade base overload functions
    #
    def draw(self):
        self.map_plan.draw()
        for enemy in self.enemies:
            enemy.draw()
        for defender in self.defenders:
            defender.draw()


    def clocked_update(self):
        if self.state == LV_PAUSED:
            self.pause()
        elif self.state == LV_PLAYING:
            self.play()
    #
    #
    #

    def pause(self):
        for e in self.enemies:
            e.pause()
        for d in self.defenders:
            d.pause()

    def play(self):
        for e in self.enemies:
            e.play()
        for d in self.defenders:
            d.play()

    def set_state(self, state: int):
        self.state = state