import arcade
import time
from drawer import LevelDrawer

class GameManager():
    DIR_DELTA = {
        arcade.key.UP: (0,1),
        arcade.key.DOWN: (0,-1),
        arcade.key.LEFT: (-1,0),
        arcade.key.RIGHT: (1, 0),
    }
    def __init__(self):
        self.drawer = LevelDrawer()
        self.activated_keys = []
        self.character_moving = False

    def update(self, delta):
        self.drawer.check_collision_and_move()
        # if self.character_moving:
        #     self.drawer.character.set_position(self.drawer.character.center_x + self.DIR_DELTA[self.activated_keys[0]][0], self.drawer.character.center_y + self.DIR_DELTA[self.activated_keys[0]][1])

    def on_key_press(self, key, modifiers):
        self.activated_keys.append(key)
        print(key)
        print("down")
        self.character_moving = True

    def on_key_release(self, key, modifiers):
        self.character_moving = False
        self.activated_keys.remove(key)
        print(key)
        print("up")