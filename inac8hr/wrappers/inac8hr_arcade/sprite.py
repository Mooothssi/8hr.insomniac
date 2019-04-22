from arcade.sprite import Sprite
from arcade.sprite_list import SpriteList
import arcade
from inac8hr.wrappers.inac8hr_arcade.legacy import ArcadeLegacy

class PreferredSprite(Sprite):
       
    def draw(self):
        if ArcadeLegacy.is_arcade_legacy("2.0.5"):
            self.internal_draw()

    def internal_draw(self):
        # self._sprite = Sprite()
        # self._sprite._texture = self._texture
        # self._sprite.textures = [self._texture]

        self._sprite_list = SpriteList()
        self._sprite_list.append(self)

        # self._sprite.center_x = self.center_x
        # self._sprite.center_y = self.center_y
        # self._sprite.width = self.width
        # self._sprite.height = self.height
        # self._sprite.angle = self.angle
        # self._sprite.alpha = self.alpha

        self._sprite_list.draw()

    def set_position(self, x, y):
        if ArcadeLegacy.is_arcade_legacy():
            super().set_position(x, y)
        else:
            super().set_position(x, y)
            #self._position = [x,y]


class ExtendedSpriteList(SpriteList):
    def insert(self, item):
        """
            Add a new sprite to the list.
        """
        idx = 0
        self.sprite_list.insert(0, item)
        self.sprite_idx[item] = idx
        item.register_sprite_list(self)
        self.vao = None
        if self.use_spatial_hash:
            self.spatial_hash.insert_object_for_box(item)