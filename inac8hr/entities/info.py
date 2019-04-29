import arcade
from inac8hr.gui import PaneTile
from i18n.loc import LocalizedText
from inac8hr.globals import GAME_PREFS

class UnitInfo:
    """
        Contains each Defender unit information
        (e.g. coverage radius, sprite assets, description)\n
        Also serves as a model of a Defender
    """
    def __init__(self):
        self.unit_name = ""
        self.strength = 1
        self.coverage_radius = 1
        self.descriptor = ""
        self.blueprint = None
        self.abilities = None


class CalculatorUnitInfo(UnitInfo):
    def __init__(self):
        self.unit_name = LocalizedText("Units/Def/Calc/Name")
        self.strength = 1
        self.coverage_radius = 1
        self.description = LocalizedText("Units/Def/Calc/Desc")
        self.blueprint = None
        self.abilities = None


VALID_PLACEMENT = 1
INVALID_PLACEMENT = 0


class UnitBlueprint():
    "Minimum of 2 texture files"
    def __init__(self, texture_files: list, scaling=1, initial_loc=(0,0)):
        self.defender = None
        self.sprite = arcade.Sprite()
        self.texture_files = texture_files
        for file_name in texture_files:
            self.sprite.append_texture(arcade.load_texture(file_name))
        self.state = INVALID_PLACEMENT
        self.configure_texture()
        self.position = initial_loc

    def set_position(self, value):
        self.sprite.set_position(*value)

    def get_position(self):
        return self.sprite.position

    position = property(get_position, set_position)

    def rescale(self):
        self.configure_texture()

    def configure_texture(self):
        self.sprite.scale = GAME_PREFS.scaling
        self.sprite.set_texture(self.state)

    def change_state(self, state):
        self.state = state
        self.configure_texture()


class In8acUnitInfo:
    """
        Unit information instance of Insomni8 Game
    """
    INFO_LIST = [
        CalculatorUnitInfo(),
    ]

    @classmethod
    def get_all(cls):
        return cls.INFO_LIST

    @classmethod
    def get_all_as_pane_tile(cls):
        return [PaneTile(model=i) for i in In8acUnitInfo.INFO_LIST]

