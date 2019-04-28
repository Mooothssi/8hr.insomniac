from arcade.sprite import Sprite
from arcade.sprite_list import SpriteList
import arcade
from inac8hr.wrappers.inac8hr_arcade.legacy import ArcadeLegacy


class DrawCommands():
    @staticmethod
    def draw_textured_rectangle(center_x: float, center_y: float, width: float,
                            height: float, texture: arcade.Texture, angle: float=0,
                            alpha: float=1,
                            repeat_count_x=1, repeat_count_y=1):
        _sprite = arcade.Sprite()
        _sprite._texture = texture
        _sprite.textures = [texture]

        _sprite_list = SpriteList()
        _sprite_list.append(_sprite)

        _sprite.center_x = center_x
        _sprite.center_y = center_y
        _sprite.width = width
        _sprite.height = height
        _sprite.angle = angle
        _sprite.alpha = alpha

        _sprite_list.draw()


class PreferredSprite(Sprite):
       
    def draw(self):
        if ArcadeLegacy.is_arcade_legacy("2.0.5"):
            self.internal_draw()

    def internal_draw(self):
        self._sprite_list = SpriteList()
        self._sprite_list.append(self)
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