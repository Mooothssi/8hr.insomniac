from inac8hr.gui import *
from inac8hr.layers import *
from inac8hr.anim import ControlAnimator, SceneSequence, SequenceInfo, ExponentialEaseOut, QuadEaseIn, TemporalSequence
from inac8hr.globals import SCR_HEIGHT, SCR_WIDTH


#
# the Jumping Ballot
#


class Level1HUD(UILayer):

    def __init__(self, manager):
        super().__init__('ui_layer')
        disp = 75
        noto = "assets/fonts/NotoSans-Regular"
        self.lblFPS = Label(Point(16, 8), font_name=noto)
        self.lblTest = Label(Point(16, 20), font_name=noto)
        self.lblStatus = Label(Point(16+disp, 8), font_name=noto)

        self.lblTest2 = Label(Point((SCR_WIDTH//2)-120,SCR_HEIGHT//2),size=20, align="center")
        self.lblTest2.text = "Jumping Ballot\n\nGet ready in 10 seconds!"

        self.lblScore = Label(Point(0,0),size=20, align="center")
        self.lblScore.text = "10"

        self.testMsg3 = AnimatedTexturedMessageBox(Point(SCR_WIDTH, SCR_HEIGHT), "assets/images/ui/pnl_Stats.png", width=424, height=288)
        self.testMsg3.alpha = 255
        self.testMsg3.centeredly_drawn = True
        self.testMsg3.add_control(self.lblScore, True)
        self.lblScore.align_center()
        self.testMsg3.position = Point(SCR_WIDTH, SCR_HEIGHT)

        self.testMsg = AnimatedTexturedMessageBox(Point(SCR_WIDTH//2,SCR_HEIGHT//2), "assets/images/chars/Ballot_pink.png")
        self.testMsg2 = AnimatedTexturedMessageBox(Point(SCR_WIDTH//2,SCR_HEIGHT//2), "assets/images/titles/lv1.png", width=507, height=315)
        self.testMsg2.add_control(self.lblTest2)
        self.manager = manager

        self.container1 = ScrollablePaneView(Point(100, 0), 640, 65)
        for _ in range(3):
            tile = Container(Point(0, 0), width=75, color=arcade.color.AMARANTH_PURPLE)
            self.container1.add_tile(tile)
            tile.click_event += self.test

        for _ in range(7):
            self.container1.add_tile(Container(Point(0, 0), width=75, color=arcade.color.AMAZON))

        self.register_control(self.lblFPS)
        self.register_control(self.container1)
        self.register_control(self.lblStatus)
        self.register_control(self.lblTest)
        self.register_control(self.testMsg2)
        self.register_control(self.testMsg3)


        seq1 = SceneSequence(self.testMsg2, [SequenceInfo("alpha", 255)], 5, ExponentialEaseOut)
        seq2 = SceneSequence(self.testMsg2, [SequenceInfo("alpha", initial_val=255, end_val=0)], 5, QuadEaseIn)
        seq_delay = TemporalSequence(5)
        seq1.started_event += self.freeze_canvas
        seq2.finished_event += self.continue_canvas
        # self.animator.subscribe_to_sequence(seq2, "on_finish", self.finish)
        self.animator.add_sequence(seq1)
        self.animator.add_sequence(seq_delay)
        self.animator.add_sequence(seq2)
        self.animator.start()
        #self.testMsg2.position = Point(500,500)

    def freeze_canvas(self, *args):
        self.lblStatus.visible = False
        self.manager.freeze_canvas()

    def continue_canvas(self, *args):
        self.lblStatus.visible = True
        self.manager.continue_canvas()

    def test(self, *args):
        print('sender')

    def test2(self, *args):
        print('sender2')
