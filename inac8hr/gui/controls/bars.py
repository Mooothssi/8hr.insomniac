from inac8hr.gui.controls import Point, Control, Container, Padding
import arcade


class ProgressBar(Container):
    def __init__(self, position: Point, width=0, height=25, indicator_color=arcade.color.DODGER_BLUE, back_color=(0, 0, 0)):
        super().__init__(position, width, height, back_color)
        self.maximum = 100
        self.minimum = 0
        self.padding = Padding(2, 2, 2, 2)
        self._value = 0
        self.indicator_color = indicator_color
        self.content_height = self.height
        self.content_width = self.width - (self.padding.right*2)
        self.__indicator_width = 12
        self.__indicator_bar__ = Container(Point(0,0), self.__indicator_width, height, self.indicator_color)
        self.add_child(self.__indicator_bar__)

    def draw(self):
        super().draw()

    def get_value(self):
        return self._value

    def set_value(self, value: int):
        if self.minimum <= value <= self.maximum:
            self._value = value
        else:
            if self.minimum > value:
                self._value = self.minimum
            elif value > self.maximum:
                self._value = self.maximum
        self._resolve_indicator_width()

    value = property(get_value, set_value)

    def _resolve_indicator_width(self):
        self.__indicator_bar__.width = (self._value / self.maximum)*self.content_width

