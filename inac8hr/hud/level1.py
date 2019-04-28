import arcade
from inac8hr.gui import *
from inac8hr.layers import *
from inac8hr.anim import ControlAnimator, SceneSequence, SequenceInfo, ExponentialEaseOut, QuadEaseIn, TemporalSequence
from inac8hr.globals import SCR_HEIGHT, SCR_WIDTH


#
# the Jumping Ballot
#


class Level1HUD(UILayer):

    def __init__(self, parent):
        super().__init__('ui_layer')
        self.parent = parent
        disp = 75
        noto = "assets/fonts/NotoSans-Regular"
        self.lblFPS = Label(Point(16, 8), font_name=noto)
        self.lblTest = Label(Point(16, 20), font_name=noto)
        self.lblStatus = Label(Point(16+disp, 8), font_name=noto)

        self.lblTest2 = Label(Point(SCR_WIDTH//2,SCR_HEIGHT//2), size=20, align=AlignStyle.BOTTOM_CENTER)
        self.lblTest2.text = "Jumping Ballot\n\nGet ready in 10 seconds!"

        #
        # Stats Panel
        #
        self.lblCycle = Label(Point(280,173), size=20, font_name=noto)
        self.lblCycle.anchors = Control.ANCHOR_RIGHT | Control.ANCHOR_TOP
        self.lblCycle.text = self.parent.lv1.cycle.current_cycle

        self.lblTurnout = Label(Point(280,150), size=20, font_name=noto)
        self.lblTurnout.anchors = Control.ANCHOR_RIGHT | Control.ANCHOR_TOP
        self.lblTurnout.text = self.parent.lv1.scoring.turnout

        # self.lblLv1Panel = Label(Point(0,0), size=20, align=AlignStyle.TOP_CENTER, color=arcade.color.WHITE)
        # self.lblLv1Panel.dock = DockStyle.TOP
        # self.lblLv1Panel.text = "8-hour insomniac:\nthe Jumping Ballot"


        self.testMsg3 = AnimatedTexturedMessageBox(Point(SCR_WIDTH-424, SCR_HEIGHT-288), "assets/images/ui/pnl_Stats.png", width=424, height=288)
        self.testMsg3.alpha = 255
        self.testMsg3.add_control(self.lblCycle, True)
        self.testMsg3.add_control(self.lblTurnout, True)
        self.testMsg3.visible = False
        # self.testMsg3.add_control(self.lblLv1Panel, True)
        self.testMsg3.position = Point(SCR_WIDTH-424, SCR_HEIGHT-288)
        #
        #
        #

        self.testMsg = AnimatedTexturedMessageBox(Point(SCR_WIDTH//2, SCR_HEIGHT//2), "assets/images/chars/Ballot_pink.png")
        self.testMsg2 = AnimatedTexturedMessageBox(Point(SCR_WIDTH//2, SCR_HEIGHT//2), "assets/images/titles/lv1.png", width=507, height=315)
        self.testMsg2.alignment = AlignStyle.MIDDLE_CENTER
        self.testMsg2.add_control(self.lblTest2)
        self.testMsg2.align_center()
        self.lblTest2.align_center()

        self.container1 = ScrollablePaneView(Point(100, 0), 640, 65)
        for _ in range(3):
            tile = PaneTile(Point(0, 0), width=75, color=arcade.color.AMARANTH_PURPLE)
            self.container1.add_tile(tile)
            tile.click_event += self.test

        for _ in range(7):
            self.container1.add_tile(PaneTile(Point(0, 0), width=75, color=arcade.color.AMAZON))

        self._register_controls()


        seq1 = SceneSequence(self.testMsg2, [SequenceInfo("alpha", 255)], 5, ExponentialEaseOut)
        seq2 = SceneSequence(self.testMsg2, [SequenceInfo("alpha", initial_val=255, end_val=0)], 5, QuadEaseIn)
        seq_delay2 = TemporalSequence(2)
        seq_delay = TemporalSequence(5)
        seq1.started_event += self.freeze_canvas
        seq2.finished_event += self.continue_canvas
        self.animator.add_sequence(seq_delay2)
        self.animator.add_sequence(seq1)
        self.animator.add_sequence(seq_delay)
        self.animator.add_sequence(seq2)
        self.animator.start()
        self.lv1 = self.parent.lv1
        self._lazy_init()

    def _register_controls(self):
        self.register_control(self.lblFPS)
        # self.register_control(self.container1)
        self.register_control(self.lblStatus)
        self.register_control(self.lblTest)
        self.register_control(self.testMsg3)
        self.register_control(self.testMsg2)

    def _lazy_init(self):
        self.lv1.cycle.cycle_changed += self.on_cycle_changed

    def on_cycle_changed(self, sender, *args):
        self.lblCycle.text = sender.current_cycle
        self.lv1.generate_enemies()

    def freeze_canvas(self, *args):
        self.lblStatus.visible = False
        self.parent.freeze_canvas()

    def continue_canvas(self, *args):
        self.lblStatus.visible = True
        self.testMsg3.visible = True
        self.parent.continue_canvas()

    def test(self, *args):
        print('sender')

    def test2(self, *args):
        print('sender2')
