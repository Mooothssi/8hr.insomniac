from .gui.controls.collections import CollectionView, DropdownItem
from .gui.controls.containers import Container
from .gui.controls.labels import LocalizedLabel
from .gui.controls.buttons import Button
from .gui import Point
from .entities.info import UnitInfo, In8acUnitInfo
from i18n.loc import LocalizedText


class CodexEntry:
    def __init__(self, thumbnail, unit_info):
        self.thumbnail = thumbnail
        self.unit_info = unit_info


class CodexCategory(CollectionView):
    class LV1:
        INTRO = 0
        CONTROLS = 1
        AGENT = 2
        INSPECTOR = 3
        PRECINCT = 4
        BALLOT_BOX = 5
        LOC_STRINGS_DICT = {
            INSPECTOR: LocalizedText('Codex/Category/Inspectors'),
            AGENT: LocalizedText('Codex/Category/Agents'),
            PRECINCT: LocalizedText('Codex/Category/Precincts'),
            INTRO: LocalizedText('Codex/Category/Intro'),
            CONTROLS: LocalizedText('Codex/Category/Controls')
        }
        @classmethod
        def get_all_as_dropdown_items(cls):
            return [DropdownItem(loc_text.key) for loc_text in cls.LOC_STRINGS_DICT.values()]

    def __init__(self, name):
        super().__init__(Point(0,0), 500, 500)
        self._background_drawn = False
        self.name = name
        self.entries = self.__items__

    @classmethod
    def lv1_get_from_preset(cls, preset: int):
        return cls(cls.LV1.LOC_STRINGS_DICT[preset])

    @classmethod
    def lv1_get_all(cls):
        categories = []
        for lv1_category in cls.LV1.LOC_STRINGS_DICT:
            categories.append(cls(cls.LV1.LOC_STRINGS_DICT[lv1_category]))
        return categories

    def add_entry(self, thumbnail, unit_info: UnitInfo):
        entry = CodexEntry(thumbnail, unit_info)
        self.__items__.append(entry)


class InspectorCategory(CodexCategory):
    def __init__(self):
        super().__init__(CodexCategory.LV1.LOC_STRINGS_DICT[CodexCategory.LV1.INSPECTOR])
        for info in In8acUnitInfo.get_all():
            self.add_entry(info.thumbnail, info)


class In8acCategories:
    ALL = [
        InspectorCategory()
    ]


class CodexBook(CollectionView):
    def __init__(self, title_label_loc: Point, desc_label_loc: Point, 
                 body_label_loc: Point, thumbnail_loc: Point, btnPrev_loc: Point,
                 btnNext_loc: Point, region, thumbnail_size: int):
        super().__init__(Point(0, 0), 500, 500)
        self._background_drawn = False
        self.title_label = LocalizedLabel(title_label_loc, size=72)
        self.description_label = LocalizedLabel(desc_label_loc)
        self.body_label = LocalizedLabel(body_label_loc)
        self.thumbnail = Container(thumbnail_loc, thumbnail_size, thumbnail_size)
        self._btnPrev = Button(btnPrev_loc,
                                "assets/images/ui/codex/btnCodexPrev.png", height=59,
                                width=42)
        self._btnNext = Button(btnNext_loc,
                                "assets/images/ui/codex/btnCodexNext.png", height=59,
                                width=42)
        self.register_drawing()
        self._region_2 = region
        self._category_lock = False

    def register_drawing(self):
        self._btnPrev.click_event += self.on_prev
        self._btnNext.click_event += self.on_next
        self.add_child(self._btnPrev)
        self.add_child(self._btnNext)
        self.children.extend([self.title_label, self.description_label, self.body_label, self.thumbnail
        ])

    def add_category(self, category):
        self.__items__.append(category)

    def _preview_first_one(self):
        info = self.selected_item.entries[0].unit_info
        self.thumbnail = info.thumbnail
        self.title_label.loc_text = info.unit_name
        self.description_label.loc_text = info.description
        self._btnPrev.visible = False
        self._btnNext.visible = True

    def on_change_info_callback(self, *args):
        info = self.selected_item.selected_item.unit_info
        self.thumbnail = info.thumbnail
        self.title_label.loc_text = info.unit_name
        self.description_label.loc_text = info.description

    def on_change_category(self, *args):
        self.select_index(args[1])
        try:
            self.selected_item.selected_index_changed_event -= self.on_change_info_callback
        except:
            pass
        self.selected_item.selected_index_changed_event += self.on_change_info_callback
        self.selected_item.select_index(0)
        self._preview_first_one()

    def on_mouse_press(self, *args):
        if self.region != self._region_2:
            self.region = self._region_2
        super().on_mouse_press(*args)

    def on_next(self, *args):
        self.selected_item.go_next()
        if self.selected_item._current_index == len(self.selected_item.items) - 1:
            self._btnNext.visible = False
            self._btnPrev.visible = True

    def on_prev(self, *args):
        self.selected_item.go_back()
        if self.selected_item._current_index == 0:
            self._btnPrev.visible = False
            self._btnNext.visible = True
