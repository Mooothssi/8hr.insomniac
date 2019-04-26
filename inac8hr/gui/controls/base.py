from inac8hr.gui.basics import Point, RectangularRegion
from inac8hr.inputs import Event, UserEvent


class Control():
    registered_inputs = [UserEvent.MOUSE_PRESS]

    def __init__(self, position: Point, width=0, height=0):
        self._position = position
        self.visible = True
        self.parent = None
        self.activated = False
        self._width = width
        self._height = height
        self.region = RectangularRegion(position, position + Point(width, 0),
                                        position + Point(width, height),
                                        position + Point(0, height))
        self.click_event = Event()

    def on_draw(self):
        if self.visible:
            self.draw()

    def draw(self):
        pass

    def clocked_update(self):
        pass

    def move_left(self, value):
        self.position.x -= value
        if value != self.position.x:
            self.reset_region()

    def move_right(self, value):
        self.position.x += value
        if value != self.position.x:
            self.reset_region()

    def get_position(self):
        return self._position

    def set_position(self, value):
        # if value - self._position != Point(0, 0):
            
        self._position = value
        self.reset_region()

    def get_width(self):
        return self._width

    def set_width(self, value):
        self._width = value
        self.reset_region()

    def get_height(self):
        return self._height

    def set_height(self, value):
        self._height = value
        self.reset_region()

    position = property(get_position, set_position)
    width = property(get_width, set_width)
    height = property(get_height, set_height)

    def show(self):
        self.visible = True
        self.on_shown()

    def on_shown(self):
        pass

    def on_mouse_press(self, *args):
        x, y, btn, modifiers = args
        self.activated = False
        if self.region.is_point_inside(Point(x, y)) and self.visible:
            self.activated = True
            self.click_event(*args)

    def reset_region(self):
        self.region = RectangularRegion(self.position,
                                        self.position + Point(self.width, 0),
                                        self.position + Point(self.width, self.height),
                                        self.position + Point(0, self.height))

    def set_region_from_center(self):
        x, y = self.position.x - (self.width / 2), self.position.y - (self.height / 2)
        position = Point(x, y)
        self.region = RectangularRegion(position, position + Point(self.width, 0),
                                        position + Point(self.width, self.height),
                                        position + Point(0, self.height))


class AnimatedControl(Control):
    pass
