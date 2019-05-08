from ..gui import *
from ..layers import UILayer
from ..anim import ControlAnimator, SceneSequence, SequenceInfo, ExponentialEaseOut, QuadEaseIn, TemporalSequence
from ..codex import CodexCategory, CodexBook, In8acCategories


class CodexLayer(UILayer):
    def __init__(self):
        super().__init__()
        self.btnSelect = Button(Point(674,424), "assets/images/ui/btnStartGame_0.png", width=603, height=109)
        self.btnSelect.append_texture("assets/images/ui/btn_SelectTool_pressed.png")
        self.btnSelect.alignment = AlignStyle.AlignXStyle.CENTER
        self.btnSelect.click += self.btnStartGame_Click

        self.bckMainMenu = AnimatedTexturedMessageBox(Point(0, 0), "assets/images/bck_main.png", width=1924, height=1080)
        self.bckMainMenu.alignment = AlignStyle.MIDDLE_CENTER
        self.bckMainMenu.align_center()

        self.bckPollingBoard = AnimatedTexturedMessageBox(Point(546, 0), "assets/images/ui/codex/bck_polling_board.png", width=1076, height=786)
        self.titleSign = AnimatedTexturedMessageBox(Point(619, 800), "assets/images/ui/codex/title_codex_sign.png", width=846, height=124)

        self.cmbSel = DropdownMenu(Point(54, 624), 385, 75, font_size=33)
        self.codexBook = CodexBook(title_label_loc=Point(757, 674), desc_label_loc=Point(1111, 332),
                                   body_label_loc=Point(1111, 164), thumbnail_size=284,
                                   btnPrev_loc=Point(626, 665), btnNext_loc=Point(1516, 665),
                                   region=self.bckPollingBoard.region,
                                   thumbnail_loc=Point(684, 214))
        for item in CodexCategory.LV1.get_all_as_dropdown_items(): 
            self.cmbSel.add(item)
        for item in In8acCategories.ALL:
            self.codexBook.add_category(item)

        
        self.cmbSel.selected_index_changed_event += self.codexBook.on_change_category_callback
        self._register_controls()

    def _register_controls(self):
        self.register_control(self.bckMainMenu)
        self.register_control(self.btnSelect)
        self.register_control(self.bckPollingBoard)
        self.register_control(self.titleSign)
        self.register_control(self.cmbSel)
        self.register_control(self.codexBook)
        self.codexBook.register_drawing()

    def btnStartGame_Click(self, sender, *args):
        self.parent.end_scene_and_go_to('MainScene')
