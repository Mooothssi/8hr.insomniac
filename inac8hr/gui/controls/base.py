from inac8hr.gui.basics import Point, Margin, RectangularRegion
from inac8hr.gui.controls.styles import DockStyle, AlignStyle
from inac8hr.events import Event, UserEvent
from inac8hr.anim import ControlAnimator


class Control():
    registered_inputs = [UserEvent.MOUSE_PRESS]

    ANCHOR_TOP = 1 << 0
    ANCHOR_LEFT = 1 << 1
    ANCHOR_RIGHT = 1 << 2
    ANCHOR_BOTTOM = 1 << 3

    def __init__(self, position: Point, width=0, height=0):
        self._position = position
        self.alignment = 0 
        self.alignment = AlignStyle.NONE
        self._anchors = self.ANCHOR_LEFT
        self.visible = True
        self.flag = False
        self.margin = Margin()
        self._parent = None
        self.activated = False
        self.centeredly_drawn = False
        self._width = width
        self._anc_dist = Margin()
        self._height = height
        self.region = RectangularRegion(position, position + Point(width, 0),
                                        position + Point(width, height),
                                        position + Point(0, height))
        self.click_event = Event(self)
        self._dock = DockStyle.NONE

    def on_draw(self):
        if self.visible:
            self.draw()

    def draw(self):
        pass

    def clocked_update(self):
        pass

    def _apply_behaviour(self):
        self._redock()
        self._realign()
        self._calc_dist()
        self._align_to_anchors()

    def _realign(self):
        if self.parent is not None:
            if self.alignment & AlignStyle.AlignXStyle.RIGHT:
                self.position.x = self.parent.position.x + self.parent.width
            if self.alignment & AlignStyle.AlignYStyle.TOP:
                self.position.y = self.parent.position.y + self.parent.height

    def _redock(self):
        if self.parent is not None:
            if self.dock == DockStyle.BOTTOM:
                self.position.y = self.parent.position.y
                self.width = self.parent.width

            elif self.dock == DockStyle.TOP:
                self.position.y = self.parent.position.y + self.parent.height
                self.width = self.parent.width


    def _calc_dist(self):
        denominator = 1
        bottom = self.position.y - self.parent.position.y #self.parent.height - self.position.y + self.height
        top = self.parent.height - bottom - self.height #bottom - (self.height // denominator)
        # print(f"{self} top: {top}")
        # left = self.parent.width - self.position.x + self.width
        # left = self.parent.width - self.width + self.parent.position.x
        left = self.position.x - self.parent.position.x
        # right = left - (self.width // denominator)
        right = self.parent.width - left - self.width
        self._anc_dist = Margin(left, bottom, top, right)

    def _align_to_anchors(self):
        if self.parent is not None:
            translated_x = self.parent.width - self._anc_dist.right - self.width + self.parent.position.x
            translated_y = self.parent.height - self._anc_dist.top - self.height + self.parent.position.y
            if self.anchors & self.ANCHOR_RIGHT:
                self.position = Point(translated_x, self.position.y)
            if self.anchors & self.ANCHOR_TOP:
                # self.position = Point(self.position.x, (self.parent.height) - self._anc_dist.top)
                self.position = Point(self.position.x, translated_y)

    def move_left(self, value):
        self.position.x -= value
        if value != self.position.x:
            self.reset_region()

    def move_right(self, value):
        self.position.x += value
        if value != self.position.x:
            self.reset_region()

    def align_center(self):
        if self._parent is not None:
            if self.alignment & AlignStyle.AlignXStyle.CENTER:
                self.position = Point(self.parent.width // 2 - self.width // 2,
                                      self.position.y)
     
            if self.alignment & AlignStyle.AlignYStyle.MIDDLE:
                self.position = Point(self.position.x,
                                      self.parent.height // 2 - self.height // 2)

#
# Getters & setters of properties
#

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

    def get_parent(self):
        return self._parent

    def set_parent(self, value):
        self._parent = value
        self._calc_dist()

    def get_anc(self):
        return self._anchors

    def set_anc(self, value):
        self._anchors |= value
        self._align_to_anchors()

    def get_dock(self):
        return self._dock

    def set_dock(self, value: DockStyle):
        self._dock = value
        self._redock()

    position = property(get_position, set_position)
    width = property(get_width, set_width)
    height = property(get_height, set_height)
    parent = property(get_parent, set_parent)
    anchors = property(get_anc, set_anc)
    dock = property(get_dock, set_dock)

#
#
#

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


class AnimatedControl():
    def __init__(self):
        self.animator = ControlAnimator()

    def tick(self):
        self.animator.update()
