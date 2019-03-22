import arcade

class LevelDrawer(arcade.Sprite):
    def __init__(self):
        self.character = arcade.Sprite('assets/images/chars/placeholder.png')
        self.character.set_position(50, 50)
        self.character.width = 50
        self.character.height = 50 

    def draw(self):
        self.character.draw()

class Character():
    def __init__(self, sprite_name):
        self.sprite = arcade.Sprite(sprite_name)