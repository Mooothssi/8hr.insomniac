import arcade
from inac8hr.gui import *
from inac8hr.layers import *
from inac8hr.anim import ControlAnimator, SceneSequence, SequenceInfo, ExponentialEaseOut, QuadEaseIn, TemporalSequence
from inac8hr.entities import In8acUnitInfo
from inac8hr.commands import CommandHandler
from inac8hr.tools import ToolHandler
from inac8hr.globals import GAME_PREFS

#
# the Jumping Ballot
#


class Level1HUD(UILayer):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        disp = 75
        noto = "assets/fonts/NotoSans-Regular"
        self.lblFPS = Label(Point(16, 8), font_name=noto)
        self.lblTest = Label(Point(16, 20), font_name=noto)
        self.lblStatus = Label(Point(16+disp, 8), font_name=noto)

        self.lblTest2 = Label(Point(GAME_PREFS.screen_width//2, GAME_PREFS.screen_height//2), size=20, align=AlignStyle.BOTTOM_CENTER)
        self.lblTest2.text = "Jumping Ballot\n\nGet ready in 10 seconds!"

#
# Stats Panel
#
        self.parent.lv1.scoring.score_changed += self.on_score_changed

        self.lblCycle = Label(Point(260,173), size=20, font_name=noto)
        self.lblCycle.anchors = Control.ANCHOR_LEFT | Control.ANCHOR_TOP
        self.lblCycle.text = self.parent.lv1.cycle.current_cycle

        self.lblTurnout = Label(Point(260,125), size=20, font_name=noto)
        self.lblTurnout.anchors = Control.ANCHOR_LEFT | Control.ANCHOR_TOP
        self.lblTurnout.text = self.parent.lv1.scoring.turnout

        self.lblVoter = Label(Point(260,77), size=20, font_name=noto)
        self.lblVoter.anchors = Control.ANCHOR_LEFT | Control.ANCHOR_TOP
        self.lblVoter.text = self.parent.lv1.scoring.voter_count

        self.lblScore = Label(Point(260,29), size=20, font_name=noto)
        self.lblScore.anchors = Control.ANCHOR_LEFT | Control.ANCHOR_TOP
        self.lblScore.text = self.parent.lv1.scoring.total

        # self.lblLv1Panel = Label(Point(0,0), size=20, align=AlignStyle.TOP_CENTER, color=arcade.color.WHITE)
        # self.lblLv1Panel.dock = DockStyle.TOP
        # self.lblLv1Panel.text = "8-hour insomniac:\nthe Jumping Ballot"


        self.testMsg3 = AnimatedTexturedMessageBox(Point(GAME_PREFS.screen_width-424, GAME_PREFS.screen_height-288), "assets/images/ui/pnl_Stats.png", width=424, height=288)
        self.testMsg3.alpha = 255
        self.testMsg3.add_control(self.lblCycle, True)
        self.testMsg3.add_control(self.lblTurnout, True)
        self.testMsg3.add_control(self.lblVoter, True)
        self.testMsg3.add_control(self.lblScore, True)
        self.testMsg3.visible = False
        # self.testMsg3.add_control(self.lblLv1Panel, True)
        self.testMsg3.position = Point(GAME_PREFS.screen_width-424, GAME_PREFS.screen_height-288)
#
#
#

#
# Side Menu Panel
#
        self.sideMenu = MenuPane(Point(0,250), "assets/images/ui/SidePane_menu.png", width=110, height=541)
        # self.sideMenu.alignment = AlignStyle.TOP_LEFT
        self.btnSelect = Button(Point(0,0), "assets/images/ui/btn_SelectTool_normal.png", width=85, height=78)
        self.btnSelect.append_texture("assets/images/ui/btn_SelectTool_pressed.png")
        self.btnSelect.alignment = AlignStyle.TOP_CENTER
        self.btnSelect.click += self.btnSelect_Click
        self.sideMenu.add_control(self.btnSelect, True)
        # Tooltip Test
        self.tlpInfo = Tooltip()
        self.tlpInfo.caption.loc_text = LocalizedText("Tools/Select/TooltipName")
        self.btnSelect.add_control(self.tlpInfo, True)
#
#
#

        self.testMsg = AnimatedTexturedMessageBox(Point(GAME_PREFS.screen_width//2, GAME_PREFS.screen_height//2), "assets/images/chars/Ballot_pink.png")
        self.testMsg2 = AnimatedTexturedMessageBox(Point(GAME_PREFS.screen_width//2, GAME_PREFS.screen_height//2), "assets/images/titles/lv1.png", width=507, height=315)
        self.testMsg2.alignment = AlignStyle.MIDDLE_CENTER
        self.testMsg2.add_control(self.lblTest)
        self.testMsg2.align_center()
        self.lblTest2.align_center()

        self.container1 = ScrollablePaneView(Point(100, 0), 640, 65)
        self.container1.selected_index_changed_event += self.test
        for e in In8acUnitInfo.get_all_as_pane_tile():
            self.container1.add_tile(e)

        for _ in range(7):
            self.container1.add_tile(PaneTile(Point(0, 0), width=75, color=arcade.color.AMAZON))

        self._register_controls()

#
# Scene sequences & animations
#
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
#
#
#

        self.tool_handler = ToolHandler(self.parent.dispatcher, self.parent.lv1)
        self.cmd_handler = CommandHandler(self.tool_handler)
        # self.parent.dispatcher.add_dispatcher(self.parent.lv1)
        self.parent.dispatcher.register_dispatcher(self.cmd_handler)
        self.parent.dispatcher.register_dispatcher(self.tool_handler)

        self.lv1 = self.parent.lv1
        self._lazy_init()

    def _register_controls(self):
        self.register_control(self.lblFPS)
        # self.register_control(self.container1)
        self.register_control(self.lblStatus)
        self.register_control(self.lblTest)
        self.register_control(self.testMsg3)
        self.register_control(self.testMsg2)
        self.register_control(self.sideMenu)

    def _lazy_init(self):
        self.lv1.cycle.cycle_changed += self.on_cycle_changed

    def draw(self):
        super().draw()
        self.tool_handler.draw()

    def on_cycle_changed(self, sender, *args):
        self.lblCycle.text = sender.current_cycle

    def freeze_canvas(self, *args):
        self.lblStatus.visible = False
        self.parent.freeze_canvas()

    def continue_canvas(self, *args):
        self.lblStatus.visible = True
        self.testMsg3.visible = True
        self.parent.continue_canvas()

    def test(self, sender, *args):
        print(sender.selected_item)

    def test2(self, *args):
        pass

    def on_score_changed(self, sender, *args):
        self.lblScore.text = sender.total
        self.lblTurnout.text = sender.turnout
        self.lblVoter.text = sender.voter_count
        if sender.jumped:
            self.lblTurnout.fore_color = arcade.color.RED
        else:
            self.lblTurnout.fore_color = arcade.color.BLACK

    def on_window_resize(self, *args):
        super().on_window_resize(*args)
        self.lv1.on_resize()

    def btnSelect_Click(self, sender, *args):
        self.parent.end_scene_and_go_to('MainScene')
        self.cmd_handler.execute_by_keyword('placement')

