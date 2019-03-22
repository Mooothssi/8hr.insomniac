import arcade

GAME_TITLE = 'Insom8ia'
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class GameManager():
    def __init__(self, mw):
        main_window = mw

    def run(self):
        arcade.run()


class InsomniaGame(arcade.Window):
    def on_draw(self):
        arcade.set_background_color(arcade.color.WHEAT)
        self.background = arcade.load_texture("assets/images/bck.png")
        arcade.start_render()
        arcade.draw_texture_rectangle(self.width, self.height, 1080, self.height, self.background)


if __name__ == '__main__':
    game = InsomniaGame(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    manager = GameManager(game)
    manager.run()

