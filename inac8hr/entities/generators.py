from inac8hr.entities import SelectableUnit, Unit, AgentUnit


class GeneratorUnit(SelectableUnit):
    DEFAULT_PER_CYCLE = 25

    def __init__(self, texture_list: list, initial_pos, scaling=1):
        super().__init__(texture_list, initial_pos, scaling)
        self.generation_factor = 1
        self.initial_pos = initial_pos
        self.agents_per_cycle = GeneratorUnit.DEFAULT_PER_CYCLE
        self.agent = None

    def generate(self, level):
        x, y = level.map_plan.get_initial_agent_position()
        initial_pos = x, y
        diff = 0
        for _ in range(4):
            files = ['Ballot_pink.png', 'Ballot_orange.png', 'Ballot_red.png']
            enemy = AgentUnit([f'assets/images/chars/{files[0]}'], initial_pos, self.full_health, GAME_PREFS.scaling, self.map_plan.switch_points)
            enemy.displace_position(0, diff)
            diff += 40
            self.enemies.append(enemy)
        self.full_health += 80

    def reset_to_full_health(self, unit, level):
        unit.reset_hp(unit.full_health * level.scoring.factor)


class SetPieceUnit():
    pass