from inac8hr.gui import *
from inac8hr.layers import *
from inac8hr.anim import ControlAnimator, SceneSequence, SequenceInfo, ExponentialEaseOut, ExponentialEaseIn
from inac8hr.globals import SCR_HEIGHT, SCR_WIDTH
#
# Ballot the Skipper
#


class Level1HUD(UILayer):

    def __init__(self):
        super().__init__('ui_layer')
        disp = 68
        self.lblFPS = Label(Point(16, 8))
        self.lblTest = Label(Point(16, 20))
        self.lblStatus = Label(Point(16+disp, 8))

        self.lblTest2 = Label(Point((SCR_WIDTH//2)-100,SCR_HEIGHT//2),size=20, align="center")
        self.lblTest2.text = "Skippy Ballots"
        self.testMsg = AnimatedTexturedMessageBox(Point(SCR_WIDTH//2,SCR_HEIGHT//2), "assets/images/chars/Ballot_pink.png")
        self.testMsg2 = AnimatedTexturedMessageBox(Point(SCR_WIDTH//2,SCR_HEIGHT//2), "assets/images/titles/lv1.png", width=507, height=315)
        self.testMsg2.add_control(self.lblTest2)

        self.register_control(self.lblFPS)
        self.register_control(self.lblStatus)
        self.register_control(self.lblTest)
        self.register_control(self.testMsg2)
        # self.register_control(self.testMsg2)

        self.animator.add_sequence(SceneSequence(self.testMsg2, [SequenceInfo("alpha", 255)], 10, ExponentialEaseOut))
        self.animator.add_sequence(SceneSequence(self.testMsg2, [SequenceInfo("alpha", initial_val=255, end_val=0)], 13, ExponentialEaseIn))
        self.animator.start()
        #self.testMsg2.position = Point(500,500)