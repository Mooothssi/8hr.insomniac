from drawer import LevelDrawer
from manager import *
import arcade

GAME_TITLE = 'Insom8ia'
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class InsomniaGame(arcade.Window):
    def __init__(self, width, height, title, manager):
        super().__init__(width, height, title)
        self.manager = manager

    def on_draw(self):
        arcade.set_background_color(arcade.color.WHEAT)
        self.background = arcade.load_texture("assets/images/bck.png")
        arcade.start_render()
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2, self.width + 500, self.height + 500, self.background)
        self.manager.drawer.draw()
        self.manager.drawer.character.draw()

    def on_key_press(self, key, modifiers):
        self.manager.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.manager.on_key_release(key, modifiers)

    def update(self, delta):
        self.manager.update(delta)

if __name__ == '__main__':
    manager = GameManager()
    game = InsomniaGame(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, manager)
    pak = TestCharRouting()
    # while True:
    #     #input()
    #     pak.check_collision_and_move()
    arcade.run()

