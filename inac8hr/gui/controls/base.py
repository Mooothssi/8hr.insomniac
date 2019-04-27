from inac8hr.gui.basics import Point, RectangularRegion
from inac8hr.events import Event, UserEvent


class Control():
    registered_inputs = [UserEvent.MOUSE_PRESS]
    ALIGN_LEFT = 0
    ALIGN_CENTER = 2

    def __init__(self, position: Point, width=0, height=0):
        self._position = position
        self.alignment = Control.ALIGN_LEFT
        self.visible = True
        self.parent = None
        self.activated = False
        self.centeredly_drawn = False
        self._width = width
        self._height = height
        self.region = RectangularRegion(position, position + Point(width, 0),
                                        position + Point(width, height),
                                        position + Point(0, height))
        self.click_event = Event(self)

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

    def align_center(self):
        if self.parent is not None:
            if self.alignment != Control.ALIGN_CENTER:
                self.position.x += self.parent.width // 2
                self.position.y += self.parent.height // 2
                self.alignment = Control.ALIGN_CENTER

    def get_position(self):
        return self._position

    def set_position(self, value):
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
        if len(args) == 4:
            x, y, btn, modifiers = args
        elif len(args) == 5:
            sender, x, y, btn, modifiers = args
        if self.region.is_point_inside(Point(x, y)) and self.visible:
            self.activated = True
            self.click_event(*args)
        else:
            self.activated = False

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
