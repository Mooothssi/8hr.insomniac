from inac8hr.manager import GameManager
from i18n.loc import LocalizedText
from inac8hr.anim import *
from pyglet.gl import *
from pyglet.window import FPSDisplay
import arcade
import time

GAME_TITLE = str(LocalizedText('Game/Title'))
SCREEN_WIDTH = 800  # 18*40
SCREEN_HEIGHT = 600  # 12*40


class InsomniaGame(arcade.Window):
    def __init__(self, width, height, title, fullscreen=False):
        super().__init__(width, height, title, fullscreen, resizable=True)
        self.manager = GameManager(resolution=(width, height))
        self.manager.load_sprites(width, height)
        self.manager.fullscreen = fullscreen
        self.fps_display = FPSDisplay(self)

    def on_draw(self):
        arcade.set_background_color(arcade.color.WHEAT)   
        self.manager.draw()
        self.fps_display.draw()

    def on_resize(self, width: float, height: float):
        super().on_resize(width, height)
        self.manager.reload_sprites(width, height)
        self.manager.on_resize(width, height)


    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.manager.fullscreen = not self.manager.fullscreen
            self.set_fullscreen(self.manager.fullscreen)
        self.manager.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        pass
        # self.manager.dispatcher.on('key_release', key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        self.manager.dispatcher.on('mouse_press', x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.manager.on_mouse_motion(x, y, dx, dy)

    def update(self, delta):
        self.manager.update(delta)

if __name__ == '__main__':
    game = InsomniaGame(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    arcade.start_render()
    arcade.run()

