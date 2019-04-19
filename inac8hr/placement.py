import arcade

VALID_PLACEMENT = 1
INVALID_PLACEMENT = 0
class PlacementAvailabilityHandler():
    def __init__(self):
        pass

    def eval_proximity(self):
        pass

class UnitBlueprint():
    "Minimum of 2 texture files"
    def __init__(self, texture_files: list):
        self.sprite = arcade.Sprite()
        for file_name in texture_files:
            self.sprite.append_texture(arcade.load_texture(file_name))
        self.state = INVALID_PLACEMENT
        self.configure_texture()
    
    def configure_texture(self):
        self.sprite.set_texture(self.state)

    def change_state(self, state):
        self.state = state
        self.configure_texture()


class UnitPlacement():
    def check_availability():
        pass