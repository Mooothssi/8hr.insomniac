from inac8hr.gui.basics import Point, Margin, RectangularRegion
from inac8hr.gui.controls.styles import DockStyle, AlignStyle
from inac8hr.events import Event, UserEvent
from inac8hr.anim import ControlAnimator
from inac8hr.wrappers.inac8hr_arcade import ExtendedSpriteList
from abc import abstractmethod
import arcade
import time

class ControlSpriteList():
    def __init__(self):
        self.sprite_list = ExtendedSpriteList()
        self.controls = []

    def draw(self):
        pass



class Control():
    registered_inputs = [UserEvent.MOUSE_PRESS, UserEvent.MOUSE_RELEASE, UserEvent.MOUSE_MOTION]
    _sprite_list_cache = arcade.SpriteList()
    ANCHOR_TOP = 1 << 0
    ANCHOR_LEFT = 1 << 1
    ANCHOR_RIGHT = 1 << 2
    ANCHOR_BOTTOM = 1 << 3

    def __init__(self, position: Point, width=0, height=0, back_color=(0, 0, 0)):
        self._position = position
        self._sprite = None
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
        self.click = Event(self)
        self.released = Event(self)
        self.double_clicked = Event(self)
        self.mouse_motion = Event(self)
        self.mouse_enter = Event(self)
        self.mouse_leave = Event(self)
        self._dock = DockStyle.NONE
        self._mouse_down = False
        self._opacity = 255
        self._mouse_enter = False
        self._mouse_enter_time = 0
        self._color = (0, 0, 0)
        self.fore_color = self._color
        self.back_color = back_color

    def dispose(self):
        if self._sprite is not None:
            Control._sprite_list_cache.remove(self._sprite)

    @staticmethod
    def draw_from_cache():
        if len(Control._sprite_list_cache) > 0:
            Control._sprite_list_cache.draw()

    def set_cached_sprite(self, sprite):
        self._sprite = sprite
        if self._sprite is not None and not self._sprite in Control._sprite_list_cache:
            Control._sprite_list_cache.append(self._sprite)

    def on_draw(self):
        if self.visible and self._sprite is None:
            self.draw()

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def tick(self):
        pass

#
# Anchor & Positioning subroutines
#

    def _apply_behaviours(self):
        self._redock()
        self._realign()
        self._calc_dist()
        self._realign_to_padding()
        self._align_to_anchors()

    def _realign(self):
        if self.parent is not None:
            if self.alignment & AlignStyle.AlignXStyle.RIGHT:
                self.position = Point(self.parent.position.x + self.parent.width - self.width - self.margin.right, self.position.y)
            if self.alignment & AlignStyle.AlignYStyle.TOP:
                self.position = Point(self.position.x, self.parent.position.y + self.parent.height - self.height - self.margin.top)
            if self.alignment & AlignStyle.AlignYStyle.MIDDLE:
                self.position.y = self.parent.position.y + (self.parent.height//2) - self.height
            if self.alignment & AlignStyle.AlignYStyle.BOTTOM:
                self.position = Point(self.position.x, self.parent.position.y + self.margin.bottom)

    def _redock(self):
        if self.parent is not None:
            if self.dock == DockStyle.BOTTOM:
                self.position.y = self.parent.position.y
                self.width = self.parent.width

            elif self.dock == DockStyle.TOP:
                self.position.y = self.parent.position.y + self.parent.height
                self.width = self.parent.width

    def _realign_to_padding(self):
        if self.parent is not None:
            if self.height > self.parent.padding.top:
                self.position.y -= self.parent.padding.top
            if self.parent.height > self.height + self.parent.padding.bottom:
                self.position.y += self.parent.padding.bottom
            if self.width > self.parent.padding.right:
                self.position.x -= self.parent.padding.right
            if self.parent.width > self.width + self.parent.padding.left:
                self.position.x += self.parent.padding.left
            if self.width > self.parent.width + self.parent.padding.left + self.parent.padding.right:
                self.width -= self.parent.padding.left + self.parent.padding.right

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

#
#
#

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

    def get_alpha(self):
        return self._opacity

    def set_alpha(self, value: int):
        r, g, b = self._color
        if len(self.fore_color) == 4:
            fore_r, fore_g, fore_b, a = self.fore_color
        else:
            fore_r, fore_g, fore_b = self.fore_color
        value = int(round(value, 0))
        # self.visible = value > 0
        self.fore_color = (fore_r, fore_g, fore_b, value)
        self.back_color = (r, g, b, value)
        self._opacity = value

    position = property(get_position, set_position)
    width = property(get_width, set_width)
    height = property(get_height, set_height)
    parent = property(get_parent, set_parent)
    anchors = property(get_anc, set_anc)
    dock = property(get_dock, set_dock)
    opacity = property(get_alpha, set_alpha)
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
            self._mouse_down = True
            self.activated = True
            self.click_event(*args)
            self.click(*args)
        else:
            self.activated = False

    def on_mouse_release(self, *args):
        if self._mouse_down:
            self._mouse_down = False
            self.released()

    def on_mouse_motion(self, *args):
        self.mouse_motion(*args)
        if len(args) == 4:
            x, y, dx, dy = args
        elif len(args) == 5:
            sender, x, y, dx, dy = args
        if self.region.is_point_inside(Point(x, y)) and self.visible:
            
            if not self._mouse_enter:
                self.mouse_enter(*args)
                self._mouse_enter = True          
                self._mouse_enter_time = time.time()
        else:
            if self._mouse_enter:
                self._mouse_enter = False
                self.mouse_leave(*args)

    def on_mouse_enter(self, *args):
        pass

    def on_mouse_leave(self, *args):
        pass 
    
    def on_window_resize(self, *args):
        pass

    def reset_region(self):
        self.region = RectangularRegion(self.position,
                                        self.position + Point(self.width, 0),
                                        self.position + Point(self.width,
                                                              self.height),
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
        self.animator.animated += self.on_animated

    def tick(self):
        self.animator.update()

    def on_animated(self, *args):
        pass

