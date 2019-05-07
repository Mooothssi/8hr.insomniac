from inac8hr.manager import GameManager
from i18n.loc import LocalizedText
from inac8hr.anim import *
import pyglet
import pyglet.clock
from pyglet.gl import *
from pyglet.window import FPSDisplay
import arcade
import time

GAME_TITLE = str(LocalizedText('Game/Title'))
SCREEN_WIDTH = 1920  # 18*40
SCREEN_HEIGHT = 1000  # 12*40


class InsomniaGame(arcade.Window):
    def __init__(self, width, height, title, fullscreen=False):
        super().__init__(width, height, title, fullscreen)
        self.manager = GameManager(resolution=(width, height))
        self.manager.load_sprites(width, height)
        self.manager.fullscreen = fullscreen
        self.label = pyglet.text.Label(str(1),
                          font_name='Times New Roman',
                          font_size=36,
                          x=width//2, y=height//2,
                          anchor_x='center', anchor_y='center')
        self.fps_display = FPSDisplay(self)

        self.config.alpha_size = 8
        self.resolution = 0, 0
        arcade.set_background_color(arcade.color.WHEAT)
        self.set_update_rate(1/144)

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()
        
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glOrtho(0, self.width, 0, self.height, -1, 1)
         
    
        self.label.draw()

        gl.glPopMatrix()

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()

    def on_resize(self, width: float, height: float):
        # super().on_resize(width, height)
        if not (self.resolution[0] == width and self.resolution[1] == height):
            self.resolution = width, height
            self.manager.reload_sprites(width, height)
            self.manager.on_resize(width, height)


    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.manager.fullscreen = not self.manager.fullscreen
            self.set_fullscreen(self.manager.fullscreen)
        elif key == arcade.key.ESCAPE:
            self.manager.fullscreen = not self.manager.fullscreen
            self.set_fullscreen(self.manager.fullscreen)
        self.manager.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        pass
        # self.manager.dispatcher.on('key_release', key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        self.manager.dispatcher.on('mouse_press', x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.manager.dispatcher.on('mouse_release', x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.manager.on_mouse_motion(x, y, dx, dy)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        super().on_mouse_scroll(x, y, scroll_x, scroll_y)

    def update(self, delta):
        # self.label.text = str(int(self.label.text) + 1)
        self.manager.update(delta)

if __name__ == '__main__':
    game = InsomniaGame(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    arcade.run()
    
