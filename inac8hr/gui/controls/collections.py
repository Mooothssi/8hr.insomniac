from inac8hr.gui.controls.base import Control, AnimatedControl
from inac8hr.gui.controls.buttons import Button
from inac8hr.gui.basics import Point
from inac8hr.events import Event
from inac8hr.gui.controls.containers import Container
import math


class CollectionView(Container):
    def __init__(self, position, width, height):
        super().__init__(position, width, height)
        self.selected_index_changed_event = Event(self)


class PaneTile(Container):
    def __init__(self, model: object):
        self.model = model


class ScrollablePaneView(CollectionView):
    DEFAULT_ITEM_LIMIT = 3
    DEFAULT_ITERATION_LIMIT = 1
    DIR_LEFT = -1
    DIR_RIGHT = 1

    def __init__(self, position, width, height):
        super().__init__(position, width, height)
        self.__items__ = []
        self.spacing = 10
        self.item_width = 50
        self.item_limit = 0
        self.click_event += self.on_click
        self._current_group_number = 1
        self._current_index = -1
        self._current_item_count = 0
        self._viewgroups = 1
        self.scroll_left_lock = False
        self.scroll_right_lock = False
        self.scroll_by = 1
        self.init_scrolling_button()

    def init_scrolling_button(self):
        x, y = self.width + self.position.x - self.spacing, self.position.y \
               + (self.height//2)
        self._btn_next = Button(Point(x, y),
                                "assets/images/ui/Next_button.png", height=75,
                                width=20)
        self._btn_next.click_event += self.on_next

        x, y = self.position.x + self.spacing, \
               self.position.y + (self.height//2)
        self._btn_prev = Button(Point(x, y),
                                "assets/images/ui/Prev_button.png", height=75,
                                width=20)
        self._btn_prev.click_event += self.on_prev
        self._btn_prev.visible = False
        self.add_child(self._btn_next)
        self.add_child(self._btn_prev)

    def draw(self):
        super().draw()

    def on_next(self, *args):
        self.scroll_left()

    def on_prev(self, *args):
        self.scroll_right()

    def add_tile(self, child: Container):
        const = 1
        if len(self.items) > 0:
            const = len(self.items) + 1
        x, y = self.get_scrollable_area()
        child.height = y
        child.position.x += self.position.x + const*self.spacing + (const-1)*child.width + x
        child.position.y += self.position.y + self.spacing
        self.add_child(child)
        self.__items__.append(child)
        if child.position.x > self.position.x + self.width - 100:
            child.visible = False
            self._current_item_count = self.item_limit
        else:
            self.item_limit += 1
        self._viewgroups = math.ceil(len(self.items)/(self.item_limit)) + 1

    def get_scrollable_area(self):
        return self._btn_next.width, self.height - (2*self.spacing)

    def on_click(self, sender, *args):
        children = zip(range(len(self.items)), self.items)
        activated = list(filter(lambda x: x[1].activated is True, children))
        if len(activated) == 1:
            self._current_index = activated[0][0]
            self.selected_index_changed_event()

    def scroll_left(self):
        self.scroll(self.DIR_LEFT)
        if self._current_group_number >= self._viewgroups:
            self._btn_next.visible = False
            self._btn_prev.visible = True
        else:
            self._current_group_number += 1
            if not self._btn_prev.visible:
                self._btn_prev.visible = True

    def scroll_right(self):
        self.scroll(self.DIR_RIGHT)
        if self._current_group_number > 1:
            self._current_group_number -= 1
            if not self._btn_next.visible:
                self._btn_next.visible = True
        elif self._current_group_number == 1:
            self._btn_prev.visible = False
            self._btn_next.visible = True

    def scroll(self, direction):
        counter = 0
        for child in self.items:
            child.move_right((self.spacing + self.items[0].width)*direction)
            if child.position.x - self.position.x <= 0:
                child.visible = False
            elif not child.position.x >= (self.position.x + self.width - self._btn_next.width):
                child.visible = True
                counter += 1
            else:
                child.visible = False
        self._current_item_count = counter

    def on_scroll(self):
        pass

    @property
    def items(self):
        return self.__items__

    @property
    def current_index(self) -> int:
        return self._current_index
