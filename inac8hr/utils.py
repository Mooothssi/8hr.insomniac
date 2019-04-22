from inac8hr.globals import GAME_PREFS


class LocationUtil():

    @staticmethod
    def get_sprite_position(r, c):
        product = GAME_PREFS.block_size * GAME_PREFS.scaling
        x = c * product + ((product) // 2)
        y = r * product + ((product) + ((product) // 2))
        return x, y

    @staticmethod
    def get_plan_position(x, y, rounded=False):
        product = GAME_PREFS.block_size * GAME_PREFS.scaling
        c = (x - (product / 2)) / product
        r = (y - ((product) + ((product) // 2))) / product
        if rounded:
            r, c = int(round(abs(r), 0)), int(round(abs(c), 0))
        return r, c
