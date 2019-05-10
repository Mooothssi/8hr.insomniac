from inac8hr.gui import *
from inac8hr.scenes.layers import *
import i18n

class MainMenuLayer(UILayer):
    def __init__(self):
        super().__init__()
        self.btnSelect = Button(Point(674,424), "assets/images/ui/btnStartGame_0.png", width=603, height=109)
        self.btnSelect.append_texture("assets/images/ui/btn_SelectTool_pressed.png")
        self.btnSelect.alignment = AlignStyle.AlignXStyle.CENTER
        self.btnSelect.click += self.btnStartGame_Click

        self.btnInstr = Button(Point(674+90,424-26-(91)), "assets/images/ui/btnInstructions_0.png", width=421, height=91)
        self.btnInstr.append_texture("assets/images/ui/btn_SelectTool_pressed.png")
        self.btnInstr.alignment = AlignStyle.AlignXStyle.CENTER
        self.btnInstr.click += self.btnInstr_Click

        self.btnQuit = Button(Point(674+90,424-26-26-(91*2)), "assets/images/ui/btnQuit.png", width=421, height=92)
        self.btnQuit.append_texture("assets/images/ui/btn_SelectTool_pressed.png")
        self.btnQuit.alignment = AlignStyle.AlignXStyle.CENTER
        self.btnQuit.click += self.btnQuit_Click

        self.bckMainMenu = AnimatedTexturedMessageBox(Point(0, 0), "assets/images/bck_main.png", width=1924, height=1080)
        self.bckMainMenu.alignment = AlignStyle.MIDDLE_CENTER
        self.bckMainMenu.align_center()

        self.btnLangTH = Button(Point(1638,295), "assets/images/ui/btnLang_th.png", width=66, height=44)
        self.btnLangTH.click += self.btnLangTH_Click

        self.btnLangEN_UK = Button(Point(1340,295), "assets/images/ui/btnLang_en_UK.png", width=66, height=44)
        self.btnLangEN_UK.click += self.btnLangEN_UK_Click





        self._register_controls()

    def _register_controls(self):
        self.register_control(self.bckMainMenu)
        self.register_control(self.btnSelect)
        self.register_control(self.btnInstr)
        self.register_control(self.btnQuit)
        self.register_control(self.btnLangTH)
        self.register_control(self.btnLangEN_UK)

    def btnStartGame_Click(self, sender, *args):
        self.parent.end_scene_and_go_to('LV1Scene')

    def btnInstr_Click(self, sender, *args):
        self.parent.end_scene_and_go_to('CodexScene')

    def btnLangTH_Click(self, sender, *args):
        i18n.Localization.instance().set_language_by_code("th_TH")
    
    def btnLangEN_UK_Click(self, sender, *args):
        i18n.Localization.instance().set_language_by_code("en_US")

    def btnQuit_Click(self, sender, *args):
        exit(0)
