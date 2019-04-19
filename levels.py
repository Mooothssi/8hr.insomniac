class Level():
    def __init__(self):
        self.map_plan = None
        self.defenders = None
        self.enemies = None
        self.state = None

    def on_draw(self):
        self.map_plan.draw()
        for enemy in self.enemies:
            enemy.draw()
        for defender in self.defenders:
            defender.draw()