from inac8hr.gui.controls.base import Control, AnimatedControl
from inac8hr.gui.controls.buttons import Button
from inac8hr.gui.basics import Point
from inac8hr.inputs import Event
from inac8hr.gui.controls.containers import Container


class CollectionView(Container):
    def __init__(self, position, width, height):
        super().__init__(position, width, height)
        self.selected_index_changed_event = Event()


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
        self.item_limit = self.DEFAULT_ITEM_LIMIT
        self.click_event += self.on_click
        self._current_index = -1
        self._current_item_count = 0
        self.scroll_left_lock = False
        self.scroll_right_lock = False
        self.init_scrolling_button()

    def init_scrolling_button(self):
        x, y = self.width + self.position.x - self.spacing, self.position.y + (self.height//2)
        self.next_button = Button(Point(x, y), "assets/images/ui/Next_button.png", height=75, width=20)
        self.click_event += self.next_button.click_event
        self.next_button.click_event += self.on_next

    def draw(self):
        super().draw()
        if self.next_button.visible:
            self.next_button.draw()

    def on_next(self, *args):
        self.scroll_left()

    def add_tile(self, child: Container):
        const = 1
        if len(self.children) > 0:
            const = len(self.children) + 1
        x, y = self.get_scrollable_area()
        child.height = y
        child.position.x += self.position.x + const*self.spacing + (const-1)*child.width + x
        child.position.y += self.position.y + self.spacing
        self.children.append(child)
        child.reset_region()
        self.add_event_handler_from_control(child)
        if child.position.x > self.position.x + self.width - 50:
            child.visible = False
            self.item_limit = len(self.children) - 1
            self._current_item_count = self.item_limit

    def get_scrollable_area(self):
        return self.next_button.width, self.height - (2*self.spacing)

    def on_click(self, *args):
        children = zip(range(len(self.children)), self.children)
        activated = list(filter(lambda x: x[1].activated is True, children))
        if len(activated) == 1:
            self._current_index = activated[0][0]
            self.selected_index_changed_event()

    def scroll_left(self):
        if self.item_limit > self._current_item_count:
            self.next_button.visible = False
            return
        self.scroll(self.DIR_LEFT)

    def scroll_right(self):
        self.scroll(self.DIR_RIGHT)

    def scroll(self, direction):
        counter = 0
        for child in self.children:
            child.move_right((self.spacing + self.children[0].width)*direction)
            if child.position.x - self.position.x <= 0:
                child.visible = False
            elif not child.position.x >= (self.position.x + self.width - self.next_button.width):
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
