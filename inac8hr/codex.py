from .gui.controls.collections import CollectionView, DropdownItem
from .entities.info import UnitInfo
from i18n.loc import LocalizedText


class CodexEntry:
    def __init__(self, thumbnail, unit_info):
        self.thumbnail = None
        self.unit_info = None


class CodexCategory(CollectionView):
    class LV1:
        INTRO = 0
        CONTROLS = 1
        AGENT = 2
        INSPECTOR = 3
        PRECINCT = 4
        BALLOT_BOX = 5
        LOC_STRINGS_DICT = {
            AGENT: LocalizedText('Codex/Category/Agents'),
            INSPECTOR: LocalizedText('Codex/Category/Inspectors'),
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


class CodexBook(CollectionView):
    def __init__(self, title_label_loc, desc_label_loc, body_label_loc):
        super().__init__(Point(0,0), 500, 500)
        self._background_drawn = False
        self.title_label = None
        self.description_label = None
        self.body_label = None
        self.thumbnail = None
        self._btnPrev = None
        self._btnNext = None

    def add_category(self, category):
        self.__items__.append(category)

    def _preview_first_one(self):
        info = self.selected_item.entries[0].unit_info
        self.thumbnail = info.thumbnail
        self.title_label.text = info.unit_name
        self.description_label.text = info.description

    def on_change_info_callback(self, *args):
        info = self.selected_item.selected_item.unit_info
        self.thumbnail = info.thumbnail
        self.title_label.text = info.unit_name
        self.description_label.text = info.description
    
    def on_change_category_callback(self, *args):
        pass
        self._preview_first_one()
