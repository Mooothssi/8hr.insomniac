import math
import arcade
from inac8hr.gui.controls import Label, Control, AnimatedControl, LocalizedLabel
from inac8hr.gui.controls.buttons import Button
from inac8hr.gui.basics import Point, Padding
from inac8hr.events import Event
from inac8hr.gui.controls.containers import Container
from inac8hr.wrappers.inac8hr_arcade import DrawCommands
from inac8hr.anim import AnimFX, AnimProperty, AnimAppearanceBehaviour, ControlSequence, QuadEaseOut


class ControlItemCollection:
    """
        Represents the collection of Control items in a CollectionView control and its derivatives
    """
    pass


class CollectionView(Container):
    """
        Represents a collective view of items
    """
    def __init__(self, position, width, height):
        super().__init__(position, width, height)
        self.selected_index_changed_event = Event(self)
        self.__items__ = []
        self._current_index = -1

    def add_item(self, item):
        self.add_child(item)
        self.__items__.append(item)

    @property
    def items(self):
        return self.__items__

    def on_mouse_press(self, *args):
        super().on_mouse_press(*args)
        children = zip(range(len(self.items)), self.items)
        activated = list(filter(lambda x: x[1].activated is True, children))
        if len(activated) == 1:
            self._current_index = activated[0][0]
            self.selected_index_changed_event()

    @property
    def current_index(self) -> int:
        return self._current_index

    @property
    def selected_item(self) -> int:
        return self.items[self._current_index]


class PaneTile(Container):
    def __init__(self, position: Point=Point(0,0), width: int=75,
                 height: int=500, model: object=None,
                 color: tuple=arcade.color.AMARANTH_PURPLE):
        super().__init__(position, width, height, color)
        self.model = model
        self.caption = Label
        self._generate_from_model()

    def _generate_from_model(self):
        if self.model is not None:
            self.thumbnail = self.model.thumbnail
        else:
            self.thumbnail = None

    def draw(self):
        super().draw()
        if self.thumbnail is not None:
            DrawCommands.draw_textured_rectangle(self.position.x + (self.width//2), 
                                                 self.position.y + (self.height//2),
                                                 self.width, self.height, self.thumbnail)
        if self.activated:
            self.region.draw()


class ScrollablePaneView(CollectionView):
    """
        A scrollable panel collection view including each item as a tile

        Args:
            position: The location of a PaneView
            width: The specified width of a PaneView
            height: The specified height of a PaneView
            item_width: The specified width of each PaneView item
            item_height: The specified height of each PaneView item
            spacing: The square inner space of a PaneView
    """
    DEFAULT_ITEM_LIMIT = 3
    DEFAULT_ITERATION_LIMIT = 1
    DIR_LEFT = -1
    DIR_RIGHT = 1

    def __init__(self, position, width, height, item_width=50, item_height=0, 
                 spacing=10):
        super().__init__(position, width, height)
        self.spacing = spacing
        self.padding = Padding(0, 0, 0, 0)
        self.item_width = item_width
        self.item_height = item_height
        self.item_limit = 0
        self._current_group_number = 1
        self._current_item_count = 0
        self._viewgroups = 1
        self.scroll_left_lock = False
        self.scroll_right_lock = False
        self.scroll_by = 1
        self.init_scrolling_button()

    def init_scrolling_button(self):
        x, y = self.width - self.spacing, 0
        self._btn_next = Button(Point(x, y),
                                "assets/images/ui/Next_button.png", height=75,
                                width=20)
        self._btn_next.click_event += self.on_next
        self._btn_next.visible = False

        self._btn_prev = Button(Point(0, 0),
                                "assets/images/ui/Prev_button.png", height=75,
                                width=20)
        self._btn_prev.click_event += self.on_prev
        self._btn_prev.visible = False
        self.add_child(self._btn_next)
        self.add_child(self._btn_prev)

    def set_background_image(self, file_name: str):
        self._texture = arcade.load_texture(file_name)

    def set_item_background_image(self, file_name):
        for item in self.__items__:
            item._texture = arcade.load_texture(file_name)

    def draw(self):
        super().draw()

    def on_next(self, *args):
        self.scroll_left()

    def on_prev(self, *args):
        self.scroll_right()

    def add_tile(self, child: PaneTile):
        const = 1
        if len(self.items) > 0:
            const = len(self.items) + 1
        x, y = self.get_scrollable_area()
        child.width = self.item_width
        if self.item_height == 0:
            child.height = y
        else:
            child.height = self.item_height
        child.position.x += (const)*self.spacing + (const-1)*child.width + x
        child.position.y += self.position.y + self.spacing
        super().add_item(child)
        if child.position.x > self.position.x + self.width - 100:
            child.visible = False
            self._current_item_count = self.item_limit
            self._btn_next.visible = True
        else:
            self.item_limit += 1
        self._viewgroups = math.ceil(len(self.items)/(self.item_limit)) + 1

    def get_scrollable_area(self):
        return self._btn_next.width, self.height - (2*self.spacing)

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
            if child.position.x <= self.position.x:
                child.visible = False
            elif child.position.x + child.width >= (self.position.x + self.width - self.spacing*2 - self._btn_next.width):
                child.visible = False
            else:
                child.visible = True
                counter += 1
        self._current_item_count = counter

    def on_scroll(self):
        pass


class MenuPane(Container):
    def __init__(self, position: Point, texture_filename: str,
                 width: int=500, height: int=500):
        super().__init__(position, width, height)
        self.texture = arcade.load_texture(texture_filename)
        self._textures = []
        self._background_drawn = False
        self.alpha = 255
        self.padding = Padding(10, 0, 45, 10)
        # self.set_region_from_center()

    def draw(self):
        DrawCommands.draw_textured_rectangle(self.position.x + (self.width//2), self.position.y + (self.height//2),
                                             self.width, self.height, self.texture, alpha=self.alpha)
        super().draw()


class DropdownItem(Container):
    def __init__(self):
        super().__init__(Point(0, 0), height=25)


class DropdownMenu(CollectionView, AnimatedControl):
    DEFAULT_ITEM_LIMIT = 5

    def __init__(self, position, width, height, item_height=75):
        super().__init__(position, width, height)
        AnimatedControl.__init__(self)
        self.padding = Padding(10, 10, 10, 10)
        self._item_height = item_height
        self._menu_container = Container(Point(0, 0), color=arcade.color.COPPER_ROSE)
        self._menu_height = DropdownMenu.DEFAULT_ITEM_LIMIT*75
        _chevron_origin = Point(self.position.x + 50, self.position.y + 50)
        _chevron_p2 = Point(self.position.x + 50, self.position.y + 50) + Point(10, 0)
        _chevron_p3 = Point(_chevron_p2.x + _chevron_origin.x // 2, self.position.y)
        # self._chevron = arcade.create_triangles_filled_with_colors([_chevron_p2, _chevron_p3, _chevron_origin], [(255, 255, 255)])

        self.caption = LocalizedLabel(Point(0, 0), size=14)
        self.text = self.caption.loc_text
        self.caption.fore_color = arcade.color.WHITE
        self.add_child(self.caption)

        self._shown_items = []
        self.click_event += self.on_click
        self._resize_menu()
        self.duration = 0.75

    def _resize_menu(self):
        self._menu_container.width = self.width
        self._menu_container.height = 0
        self._menu_container.position = Point(self.position.x, self.position.y + 1)
        self._menu_container.visible = False
        # self.add_child(self._menu_container)

    def on_animated(self, *args):
        self._menu_container.position = Point(self._menu_container.position.x, self.position.y - self._menu_container.height + 1)
        for item in self.__items__:
            if item.position.y > self._menu_container.position.y + self._menu_container.height:
                item.visible = False
            else:
                item.visible = True

    def add(self, child: DropdownItem):
        const = 1
        if len(self.items) > 0:
            const = len(self.items) + 1
        self.__items__.append(child)
        if const % 2 == 0:
            child.back_color = arcade.color.WATERSPOUT
        else:
            child.back_color = arcade.color.WILD_WATERMELON
        child.width = self.width
        child.height = self._item_height
        child.position.y = self._menu_height - (const)*child.height
        child.visible = False
        child._lower = False
        self._menu_container.add_child(child)
        if const > DropdownMenu.DEFAULT_ITEM_LIMIT:
            child._lower = True

    def on_click(self, *args):
        self.on_open_dropdown()

    def _generate_sequences(self, prefab):
        self.animator.add_sequence(ControlSequence(self._menu_container, self.duration, prefab))

    def start_scrolling_out_menu(self, end_val):
        self._menu_container.visible = True
        prefab = AnimFX(0, AnimProperty.Height, AnimAppearanceBehaviour.NONE,
                        end_val, QuadEaseOut)
        self.animator.reset()
        self._generate_sequences(prefab)
        self.animator.start()

    def tick(self):
        AnimatedControl.tick(self)

    def on_open_dropdown(self):
        self.start_scrolling_out_menu(self._menu_height)
        for item in self.__items__:
            if not item._lower:
                item.visible = True

    def close_menu(self):
        self.start_scrolling_out_menu(0)
        for item in self.__items__:
            item.visible = False

    def on_mouse_press(self, *args):
        super().on_mouse_press(*args)
        if not self.activated:
            self.close_menu()

    def draw(self):
        if self._menu_container.visible:
            self._menu_container.draw()
        # self._chevron.draw()
        super().draw()
