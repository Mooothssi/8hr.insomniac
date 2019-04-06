import arcade
import time
from drawer import LevelDrawer, Character

class GameManager():
    DIR_DELTA = {
        arcade.key.UP: (0,1),
        arcade.key.DOWN: (0,-1),
        arcade.key.LEFT: (-1,0),
        arcade.key.RIGHT: (1, 0),
    }
    def __init__(self, resolution):
        self.drawer = LevelDrawer()
        width, height = resolution
        self.screen_width = width
        self.screen_height = height
        self.activated_keys = []
        self.character_moving = False
        self.cursor = Character('assets/images/chars/placeholder.png',(-5,-5))
        self.cursor_pos = (0,0)
        self.cursor.sprite.scale = 0.5
        self.fps = 0
        self.scaling = 1

    def load_sprites(self, width, height):
        self.screen_width = width
        self.screen_height = height
        self.scaling = (width)/(self.drawer.width*self.drawer.block_size)
        self.drawer.load_sprites(self.scaling)

    def update(self, delta):
        self.fps = 1/delta
        
        print("--")
        #self.drawer.check_collision_and_move(self.drawer.character)

        self.drawer.update()
        self.cursor.set_position(self.cursor_pos[0],self.cursor_pos[1])
        
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


    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        self.cursor_pos = x,y
        # Move the center of the player sprite to match the mouse x, y
      