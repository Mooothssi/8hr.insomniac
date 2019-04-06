import arcade
import collections
import time
from drawer import LevelDrawer, Character

class FPSCounter:
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=60)

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)

class GameManager():
    DIR_DELTA = {
        arcade.key.UP: (0,1),
        arcade.key.DOWN: (0,-1),
        arcade.key.LEFT: (-1,0),
        arcade.key.RIGHT: (1, 0),
    }
    def __init__(self, resolution):
        self.drawer = LevelDrawer()
        self.fullscreen = False
        width, height = resolution
        self.screen_width = width
        self.screen_height = height
        self.activated_keys = []
        self.character_moving = False
        self.background = arcade.load_texture("assets/images/bck.png")
        self.cursor = Character('assets/images/chars/placeholder_neutral.png',(-5,-5))
        self.cursor_pos = (0,0)
        self.cursor.sprite.scale = 0.5
        self.cursor.sprite.alpha = 0.5
        self.fps = FPSCounter()
        self.scaling = 1

    def draw(self):
        arcade.draw_texture_rectangle(self.screen_width // 2, self.screen_height // 2, self.screen_width + 500, self.screen_height + 500, self.background)
        self.drawer.draw()
        self.cursor.draw()
        arcade.draw_text(f"FPS: {self.fps.get_fps():.2f} | Scaling: {self.scaling:.2f}", 16, 8, arcade.color.BLACK)

    def load_sprites(self):
        self.reset_scaling(self.screen_width, self.screen_height)
        self.drawer.load_sprites(self.scaling)
        
    def reset_scaling(self, width, height):
        self.screen_width, self.screen_height = width, height
        import math
        width_ratio = width / (self.drawer.width*self.drawer.block_size)
        height_ratio = height  / (self.drawer.height*self.drawer.block_size)
        diff = math.log((((width_ratio*9) + (height_ratio*1)) / 10), 10)*2.2
        self.scaling = 1 + diff

    def update(self, delta):
        print(1/delta)
        print("--")
        #self.drawer.check_collision_and_move(self.drawer.character)
        # self.drawer.update()
        # self.cursor.set_position(self.cursor_pos[0],self.cursor_pos[1])
        self.fps.tick()
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
      