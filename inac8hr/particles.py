import arcade
from inac8hr.physics import CirclePhysicsEntity
from inac8hr.utils import LocationUtil


class Particle(CirclePhysicsEntity):
    def __init__(self, sprite_name, initial_pos=(0, 0), scaling=1):
        x, y = LocationUtil.get_sprite_position(*initial_pos)
        # TODO: Absolute and Relative position
        self.sprite_name = sprite_name
        self.sprite = arcade.Sprite(sprite_name)
       
        self.scaling = scaling
        self.sprite.width = 18
        self.sprite.height = 18
        self.dead = False
        super().__init__([x, y], 9)
        self.sprite.change_x = 5
        self.sprite.change_y = 5

    def draw(self):
        self.sprite.draw()

    def play(self):
        self.sprite.update()
    
    def pause(self):
        pass

    def get_x1(self):
        return self.sprite.position[0]

    def set_x1(self, value):
        self.sprite.center_x = value

    def get_y1(self):
        return self.sprite.position[1]

    def set_y1(self, value):
        self.sprite.center_y = value
    
    x1 = property(get_x1, set_x1)
    y1 = property(get_y1, set_y1)


class Bullet(Particle):
    PROXIMITY_THRESHOLD = 3
    def __init__(self, sprite_name, initial_pos=(0,0)):
        super().__init__(sprite_name, initial_pos)
        r, c = initial_pos
        x, y = LocationUtil.get_sprite_position(r, c)
        self.initial_pos = x, y
        self.sprite.set_position(x, y)
        self.fired = False
        self.disarmed = False
        self.velocity = 2
        self.target_pos = (0, 0)

    def to(self, pos):
        self.target_pos = pos
        change_x = pos[0] - self.x1
        change_x /= abs(change_x)
        change_y = pos[1] - self.y1
        change_y /= abs(change_y)
        self.sprite.change_x = self.velocity*change_x
        self.sprite.change_y = self.velocity*change_y

    def play(self):
        super().play()
        x1, y1 = self.target_pos
        x2, y2 = self.x1, self.y1
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        if 0 <= dx <= self.PROXIMITY_THRESHOLD and 0 <= dy <= self.PROXIMITY_THRESHOLD:
            self.dispose()

    def dispose(self):
        self.disarmed = True
        self.x1, self.y1 = self.initial_pos