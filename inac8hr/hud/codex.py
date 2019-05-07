from inac8hr.gui import *
from inac8hr.layers import UILayer
from inac8hr.anim import ControlAnimator, SceneSequence, SequenceInfo, ExponentialEaseOut, QuadEaseIn, TemporalSequence


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

        self.cmbSel = DropdownMenu(Point(54, 624), 385, 75)
        self.it1 = DropdownItem()
        self.cmbSel.add(self.it1)
        self.cmbSel.add(DropdownItem())
        self.cmbSel.add(DropdownItem())
        self._register_controls()

    def _register_controls(self):
        self.register_control(self.bckMainMenu)
        self.register_control(self.btnSelect)
        self.register_control(self.cmbSel)
        self.register_control(self.bckPollingBoard)
        self.register_control(self.titleSign)

    def btnStartGame_Click(self, sender, *args):
        pass

