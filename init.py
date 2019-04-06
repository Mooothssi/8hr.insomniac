from drawer import LevelDrawer
from manager import GameManager
import arcade

GAME_TITLE = 'Insom8ia'
SCREEN_WIDTH = 800#18*40
SCREEN_HEIGHT = 600#12*40

class InsomniaGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.manager = GameManager(resolution=(width,height))
        self.manager.load_sprites(width, height)

    def on_draw(self):
        arcade.set_background_color(arcade.color.WHEAT)
        self.background = arcade.load_texture("assets/images/bck.png")
        arcade.start_render()
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2, self.width + 500, self.height + 500, self.background)
        arcade.draw_text(f"FPS: {self.manager.fps:.2f} | Scaling: {self.manager.scaling:.2f}", 16, 8, arcade.color.BLACK)
        self.manager.drawer.draw()
        self.manager.cursor.draw()

    def on_key_press(self, key, modifiers):
        self.manager.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.manager.on_key_release(key, modifiers)
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.manager.on_mouse_motion(x, y, dx, dy)

    def update(self, delta):
        self.manager.update(delta)

if __name__ == '__main__':
    game = InsomniaGame(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    arcade.run()

