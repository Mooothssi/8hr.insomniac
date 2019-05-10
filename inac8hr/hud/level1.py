from inac8hr.gui import *
from inac8hr.scenes.layers import *
from inac8hr.anim import SceneSequence, SequenceInfo, ExponentialEaseOut, QuadEaseIn, TemporalSequence
from inac8hr.entities import In8acUnitInfo
from inac8hr.commands import CommandHandler
from inac8hr.tools import ToolHandler
from inac8hr.globals import GAME_PREFS
import i18n

#
# the Jumping Ballot
#
# TODO: Add an InspectorPanel.
#


class Level1HUD(UILayer):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        disp = 75
        noto = "assets/fonts/NotoSans-Regular"
        self.lblFPS = Label(Point(16, 20), font_name=noto, cached=False)
        self.lblTest = Label(Point(86, 20), font_name=noto)
        self.lblStatus = LocalizedLabel(Point(16+disp, 8), "Intro/Instructions")
        self.lblTotalScore = Label(Point(1065, 650-56), font_name=noto, size=78, color=arcade.color.WHITE)
        self.lblTotalScore.visible = False

        self.lblTest2 = Label(Point(GAME_PREFS.screen_width//2, GAME_PREFS.screen_height//2), size=20)
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
        self.testMsg3.anchors |= Control.ANCHOR_RIGHT | Control.ANCHOR_TOP
        self.testMsg3.set_region_from_center()
        self.testMsg3.add_control(self.lblCycle, True)
        self.testMsg3.add_control(self.lblTurnout, True)
        self.testMsg3.add_control(self.lblVoter, True)
        self.testMsg3.add_control(self.lblScore, True)
        self.testMsg3.visible = False
        # self.testMsg3.add_control(self.lblLv1Panel, True)
        self.testMsg3.position = Point(GAME_PREFS.screen_width-424, GAME_PREFS.screen_height-288)

        self.pgbTest = ProgressBar(Point(0,680), 243, 25)
        self.pgbTest.margin = Margin(0,0,0,5)
        self.pgbTest.alignment = AlignStyle.AlignXStyle.RIGHT
        self.pgbTest.visible = False
#
#
#

#
# Side Menu Panel
#
        self.sideMenu = MenuPane(Point(0,250), "assets/images/ui/SidePane_menu.png", width=110, height=541)

        self.btnSelect = MenuButton(Point(0,0), "assets/images/ui/btn_SelectTool_normal.png", width=85, height=78)
        self.btnSelect.append_texture("assets/images/ui/btn_SelectTool_pressed.png")
        self.btnSelect.alignment = AlignStyle.TOP_CENTER
        self.btnSelect.click += self.btnSelect_Click

        self.btnPlace = MenuButton(Point(0,0), "assets/images/ui/btnPlace_0.png", width=85, height=78)
        self.btnPlace.append_texture("assets/images/ui/btnPlace_1.png")
        self.btnPlace.alignment = AlignStyle.TOP_CENTER
        self.btnPlace.margin = Margin(0,0,78+17,0)
        self.btnPlace.click += self.btnPlace_Click

        self.btnToMainMenu = MenuButton(Point(0,0), "assets/images/ui/btnHbgrMenu_0.png", width=86, height=78)
        self.btnToMainMenu.append_texture("assets/images/ui/btnHbgrMenu_1.png")
        self.btnToMainMenu.alignment = AlignStyle.BOTTOM_CENTER
        self.btnToMainMenu.margin = Margin(0,60,0,0)
        self.btnToMainMenu.click += self.btnToMainMenu_Click

        self.sideMenu.add_control(self.btnSelect, True)
        self.sideMenu.add_control(self.btnPlace, True)
        self.sideMenu.add_control(self.btnToMainMenu, True)

        self.btnSelect.set_localized_tooltip("Tools/Select/TooltipName")
        self.btnPlace.set_localized_tooltip("Tools/Place/TooltipName")
        self.btnToMainMenu.set_localized_tooltip("Tools/Exit/TooltipName")

#
#
#

        self.testMsg = AnimatedTexturedMessageBox(Point(GAME_PREFS.screen_width//2, GAME_PREFS.screen_height//2), "assets/images/chars/Ballot_pink.png")
        self.testMsg2 = AnimatedTexturedMessageBox(Point(GAME_PREFS.screen_width//2, GAME_PREFS.screen_height//2), "assets/images/titles/lv1.png", width=507, height=315)
        self.testMsg2.alignment = AlignStyle.MIDDLE_CENTER
        self.testMsg2.alpha = 0
        self.testMsg2.align_center()
        self.testMsg2.add_control(self.lblTest2)



        self.awakeMsg = AnimatedTexturedMessageBox(Point(0, 0), "assets/images/titles/awake_screen.png", width=1920, height=1000)
        self.awakeMsg.alpha = 255
        self.awakeMsg.alignment = AlignStyle.MIDDLE_CENTER
        self.awakeMsg.align_center()
        self.awakeMsg.visible = False

        self.btnMM = Button(Point(683, 394), "assets/images/ui/btnExitToMM.png", width=655, height=109)
        self.btnMM.append_texture("assets/images/ui/btnExitToMM.png")
        self.btnMM.alignment = AlignStyle.AlignXStyle.CENTER
        self.btnMM.click += self.btnToMM_Click
        self.btnMM.visible = False

#
#  Unit placement selection view
#

        self.container1 = ScrollablePaneView(Point(200, 0), 338, 109, 81, 81, 11)
        self.container1.set_background_image("assets/images/ui/pnlSelectAgent.png")
        self.container1.visible = False
        self.container1.selected_index_changed_event += self.on_select_blueprint
        for e in In8acUnitInfo.get_all_as_pane_tile():
            self.container1.add_tile(e)
        self.container1.set_item_background_image("assets/images/ui/pnlSelectUnitItem.png")
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
        self.parent.dispatcher.register_dispatcher(self.cmd_handler)
        self.parent.dispatcher.register_dispatcher(self.tool_handler)

        self.lv1 = self.parent.lv1
        self.lv1.cycle.cycle_changed += self.on_cycle_changed
        self.lv1.cycle.cycle_end += self.on_cycle_end
        self.pgbTest.maximum = self.lv1.cycle.game_time_limit

    def _register_controls(self):
        self.register_control(self.lblFPS)
        self.register_control(self.container1)
        self.register_control(self.lblStatus)
        self.register_control(self.lblTest)
        self.register_control(self.testMsg3)
        self.register_control(self.testMsg2)
        self.register_control(self.sideMenu)
        self.register_control(self.pgbTest)
        self.register_control(self.awakeMsg)
        self.register_control(self.btnMM)
        self.register_control(self.lblTotalScore)

    def draw(self):
        self.tool_handler.draw()
        super().draw()

    def on_cycle_changed(self, sender, *args):
        self.lblCycle.text = sender.current_cycle
        self.lblVoter.text = self.lv1.scoring.voter_count

    def freeze_canvas(self, *args):
        self.lblStatus.visible = False
        self.parent.freeze_canvas()

    def continue_canvas(self, *args):
        self.lblStatus.visible = True
        self.testMsg3.visible = True
        self.pgbTest.visible = True
        self.parent.continue_canvas()

    def on_select_blueprint(self, sender, *args):
        if self.tool_handler.is_tool_utilized('placement') and sender.selected_item.model is not None:
            self.tool_handler.current_tool.change_blueprint(sender.selected_item.model)

    def on_cycle_end(self, *args):
        self.parent.freeze_canvas()
        self.awakeMsg.visible = True
        self.btnMM.visible = True
        self.lblTotalScore.text = self.lblScore.text
        self.lblTotalScore.visible = True

    def on_score_changed(self, sender, *args):
        self.lblVoter.text = sender.voter_count
        self.lblScore.text = sender.total
        self.lblTurnout.text = str(sender.turnout)
        if sender.jumped:
            self.lblTurnout.fore_color = arcade.color.RED
            self.lblTurnout.text += " (Jumped!)"
        else:
            self.lblTurnout.fore_color = arcade.color.BLACK

    def on_window_resize(self, *args):
        super().on_window_resize(*args)
        self.lv1.on_resize()

    def btnSelect_Click(self, sender, parent, x, y, button, *args):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.cmd_handler.execute_by_keyword('select')
            i18n.Localization.instance().set_language_by_code("th_TH")

    def btnPlace_Click(self, sender, parent, x, y, button, *args):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.cmd_handler.execute_by_keyword('placement')
            self.container1.visible = not self.container1.visible

    def btnToMainMenu_Click(self, sender, parent, x, y, button, *args):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.parent.end_scene_and_go_to('MainScene')

    def btnToMM_Click(self, sender, parent, x, y, button, *args):
        self.parent.end_scene_and_go_to('MainScene')

    def tick(self):
        super().tick()
        if self.lv1.cycle.started:
            self.pgbTest.value = self.lv1.cycle.get_time_remaining()
