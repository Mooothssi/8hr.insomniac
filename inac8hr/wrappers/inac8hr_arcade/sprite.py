from arcade.sprite import Sprite
from inac8hr.wrappers.inac8hr_arcade.legacy import ArcadeLegacy

class PreferredSprite(Sprite):
    def set_position(self, x, y):
        if ArcadeLegacy.is_arcade_legacy():
            super().set_position(x, y)
        else:
            super().set_position(x, y)
            #self._position = [x,y]