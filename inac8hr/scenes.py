from inac8hr.layers import SceneLayer
import arcade


class Scene():

    def __init__(self, ui_layer: SceneLayer, canvas_layer: SceneLayer,
                 tool_layer: SceneLayer):
        self.layers = {}
        self.layers_coll = []
        # TODO: Animation sequences for each scene (Loading, Popup backdrop, etc.)
        self.sequences = []
        self.append_layer(canvas_layer)
        self.append_layer(ui_layer)

    def draw(self):
        for layer in self.layers_coll:
            layer.draw()

    def clocked_update(self):
        for layer in self.layers_coll:
            layer.clocked_update()

    def get(self, key):
        return self.layers_coll[self.layers[key]]

    def pause(self):
        self.get('canvas_layer').pause()

    def play(self):
        self.get('canvas_layer').play()

    def append_layer(self, layer: SceneLayer):
        if layer.name in self.layers:
            self.replace_layer(layer)
        else:
            self.layers_coll.append(layer)
            self.layers[layer.name] = len(self.layers_coll) - 1

    def replace_layer(self, layer: SceneLayer):
        index = self.layers[layer.name]
        self.layers_coll.pop(index)
        self.layers_coll.insert(index, layer) 

    def delete_layer(self, layer_name: str):
        index = self.layers[layer_name]
        self.layers_coll.pop(index)
        self.layers_coll.insert(index, None)


class Viewport():
    def __init__(self, initial_scene: Scene):
        self.current_scene = initial_scene

    def draw(self):
        self.current_scene.draw()

    def clocked_update(self):
        self.current_scene.clocked_update()
