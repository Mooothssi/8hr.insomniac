from threading import Thread
from multiprocessing.pool import ThreadPool
from i18n.loc import LocalizedText

GAME_TITLE = str(LocalizedText('Game/Title'))
SCREEN_WIDTH = 1920  # 18*40
SCREEN_HEIGHT = 1000  # 12*40

def create_window():
    from inac8hr.window import InsomniaGame, arcade
    game = InsomniaGame(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    arcade.run()

if __name__ == '__main__':
    create_window()
