from inac8hr.layers import SceneLayer

class Scene():

    def __init__(self, ui_layer: SceneLayer, canvas_layer: SceneLayer):
        self.ui_layer = ui_layer
        self.canvas_layer = canvas_layer

    def draw(self):
        self.ui_layer.draw()
        self.canvas_layer.draw()

    def clocked_update(self):
        self.ui_layer.update()
        self.canvas_layer.update()

    def pause(self):
        self.canvas_layer.pause()

    def play(self):
        self.canvas_layer.play()


class Viewport():
    def __init__(self, initial_scene: Scene):
        self.current_scene = initial_scene

    def draw(self):
        self.current_scene.draw()

    def clocked_update(self):
        self.current_scene.clocked_update()