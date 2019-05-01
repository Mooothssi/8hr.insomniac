from inac8hr.gui import *
from inac8hr.layers import *
from inac8hr.anim import ControlAnimator, SceneSequence, SequenceInfo, ExponentialEaseOut, QuadEaseIn, TemporalSequence


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

        self.btnQuit = Button(Point(674+90,424-26-26-(91*2)), "assets/images/ui/btnQuit.png", width=421, height=92)
        self.btnQuit.append_texture("assets/images/ui/btn_SelectTool_pressed.png")
        self.btnQuit.alignment = AlignStyle.AlignXStyle.CENTER
        self.btnQuit.click += self.btnQuit_Click

        self.pgbTest = ProgressBar(Point(0,0), 243, 75)
        self.pgbTest.alignment = AlignStyle.AlignXStyle.CENTER
        self.pgbTest.value = 12

        self._register_controls()

    def _register_controls(self):
        self.register_control(self.btnSelect)
        self.register_control(self.btnInstr)
        self.register_control(self.btnQuit)
        self.register_control(self.pgbTest)

    def btnStartGame_Click(self, sender, *args):
        self.parent.end_scene_and_go_to('LV1Scene')

    def btnQuit_Click(self, sender, *args):
        exit(0)
