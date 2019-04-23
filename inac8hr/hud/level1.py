from inac8hr.gui import *
from inac8hr.layers import *
from inac8hr.anim import ControlAnimator, SceneSequence, SequenceInfo, ExponentialEaseOut
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
        self.testMsg = AnimatedTexturedMessageBox(Point(8,9), "assets/images/chars/Ballot_pink.png")
        self.testMsg2 = AnimatedTexturedMessageBox(Point(50,50), "assets/images/chars/Ballot_pink.png")

        self.register_control(self.lblFPS)
        self.register_control(self.lblStatus)
        self.register_control(self.lblTest)
        # self.register_control(self.testMsg)
        # self.register_control(self.testMsg2)

        # self.animator.add_sequence(SceneSequence(self.testMsg, [SequenceInfo("alpha", 225)], 10, ExponentialEaseOut))
        # self.animator.add_sequence(SceneSequence(self.testMsg2, [SequenceInfo("alpha", 225)], 10, ExponentialEaseOut))
        self.animator.start()
