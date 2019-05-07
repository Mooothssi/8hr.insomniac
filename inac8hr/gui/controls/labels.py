import arcade
import pyglet
import time
from i18n.loc import LocalizedText
from inac8hr.wrappers.inac8hr_arcade import DrawCommands, PILText
from inac8hr.gui.controls.base import Control, AnimatedControl
from inac8hr.gui.controls.containers import Container
from inac8hr.gui.basics import Point, Padding
from inac8hr.anim import ControlSequence, AnimFXPrefabs
from inac8hr.gui.controls.styles import AlignStyle


class Label(Control):
    _sprite_list_cache = arcade.SpriteList()

    def __init__(self, position: Point=Point(0, 0), text: str="",
                 size: int=12, color: tuple=arcade.color.BLACK, align: AlignStyle=AlignStyle.NONE, font_name=('calibri','arial'),
                 cached=False):
        super().__init__(position)
        self.__label__ = pyglet.text.Label(text, font_size=size, x=position.x,
                                           y=position.y)
        self.alignment = align
        self._text = text
        r, g, b = color
        self._color = color
        self.fore_color = (r, g, b, self.opacity)
        self._font_name = font_name
        self.__font_size__ = size
        self.cached = cached
        self.width, self.height = PILText.determine_dimensions(self, self.text)
        if self.cached and self.visible:
            self.set_cached_sprite(PILText.render_text(self.text, self.position.x, self.position.y,
                                    self.fore_color, self.font_size, font_name=self.font_name,
                                    align=self._get_text_alignment(), width=self.width, anchor_x=self._get_anchors_x(),
                                    anchor_y=self._get_anchors_y()))  

    @property
    def font_size(self):
        return self.__font_size__

    def set_text(self, value):
        self._text = value
        # if self.cached and self.visible:
        #     self.set_cached_sprite(CreateText.render_text(str(self.text), self.position.x, self.position.y,
        #                             self.fore_color, self.font_size, font_name=self.font_name,
        #                             align=self._get_text_alignment(), width=self.width, anchor_x=self._get_anchors_x(),
        #                             anchor_y=self._get_anchors_y())) 

    def get_text(self):
        return self._text

    text = property(get_text, set_text)

    def draw(self):
        if self.text != "" and self.visible and not self.cached:
            PILText.draw_text(self, str(self.text), self.position.x, self.position.y,
                             self.fore_color, self.font_size, font_name=self.font_name,
                             align=self._get_text_alignment(), anchor_x=self._get_anchors_x(),
                             anchor_y=self._get_anchors_y())

    def _get_text_alignment(self):
        if self.alignment & AlignStyle.AlignXStyle.CENTER:
            return "center"
        elif self.alignment & AlignStyle.AlignXStyle.RIGHT:
            return "right"
        else:
            return "left"

    def _get_anchors_x(self):
        if self.anchors & self.ANCHOR_RIGHT:
            return "right"
        else:
            return "left"

    def _get_anchors_y(self):
        if self.alignment & AlignStyle.AlignYStyle.TOP:
            return "top"
        else:
            return "bottom"

    def get_font_name(self):
        return self._font_name

    def set_font_name(self, value):
        self._font_name = value

    font_name = property(get_font_name, set_font_name)


class LocalizedLabel(Label):
    def __init__(self, position: Point, key: str="LocalizedText/None",
                 size: int=12):
        self.loc_text = LocalizedText(key)
        super().__init__(position, key, size)

    def get_text(self):
        return str(self.loc_text)

    def set_text(self, value):
        self._text = value

    def get_font_name(self):
        return self.loc_text.locale.get_localized_font_name()

    text = property(get_text, set_text)
    font_name = property(get_font_name, Label.set_font_name)


class Tooltip(Container, AnimatedControl):
    def __init__(self, color: tuple=arcade.color.BLACK, width: int=75, height: int=30, duration: float=0.35, text=""):
        super().__init__(Point(0, 0), width, height)
        AnimatedControl.__init__(self)
        self._background_drawn = True
        self._color = color
        self.padding = Padding(10, 10, 10, 10)
        r, g, b = color
        self.back_color = (r, g, b, 0)
        self.caption = LocalizedLabel(Point(0, 0), size=14)
        self.text = self.caption.loc_text
        self.caption.fore_color = arcade.color.WHITE
        self.add_child(self.caption)
        self.opacity = 0
        self.duration = duration
        self.await_duration = 0.5
        self._triggered = False
        self.visible = True
        self._shape_list = arcade.ShapeElementList()
        SCREEN_WIDTH = 1920
        SCREEN_HEIGHT = 1000
        self._shape_list.center_x = SCREEN_WIDTH // 2
        self._shape_list.center_y = SCREEN_HEIGHT // 2
        self._append_to_shape_list()
        self._autosize()

    def _generate_sequences(self, prefab):
        self.animator.add_sequence(ControlSequence(self, self.duration, prefab))

    def _autosize(self):
        self.width = self.caption.width + self.padding.left + self.padding.right

    def draw(self):
        super().draw()
        self._autosize()

    def _append_to_shape_list(self):
        shape = arcade.create_rectangle_filled(self.position.x + (self.width//2), self.position.y,
                                               self.width, self.height, self.back_color)
        self._shape_list.append(shape)

    def fade(self, prefab):
        self.animator.reset()
        self._generate_sequences(prefab)
        self.animator.start()

    def tick(self):
        AnimatedControl.tick(self)
        if self._triggered and time.time() - self._mouse_enter_time > self.await_duration:
            self._triggered = False
            self.fade(AnimFXPrefabs.FadeInTooltip)

    def on_mouse_enter(self, *args):
        x, y, dx, dy = args[-4], args[-3], args[-2], args[-1]
        self.position = Point(x, y)
        self._mouse_enter_time = time.time()
        self._triggered = True

    def on_mouse_leave(self, *args):
        self._triggered = False
        self.fade(AnimFXPrefabs.FadeOut)

    def on_mouse_press(self, *args):
        pass

    def on_mouse_motion(self, *args):
        pass

    @property
    def triggered(self):
        pass

    def set_alpha(self, value: int):
        super().set_alpha(value)

    opacity = property(Container.get_alpha, set_alpha)
