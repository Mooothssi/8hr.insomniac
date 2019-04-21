from inac8hr.gui import *
from inac8hr.layers import *

#
# Ballot the Skipper
#


class Level1HUD(UILayer):

    def __init__(self):
        super().__init__('ui_layer')
        disp = 68
        self.lblFPS = Label(Point(16, 8))
        self.lblStatus = Label(Point(16+disp, 8))
        #self.lblStatus.text = "Loading..."
        ##
        self.register_control(self.lblFPS)
        self.register_control(self.lblStatus)