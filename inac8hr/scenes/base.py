from inac8hr.layers import SceneLayer
from inac8hr.events import Event
import arcade


class Scene():

    def __init__(self, *args: SceneLayer):
        self.layers = {}
        self.layers_coll = []
        # TODO: Animation sequences for each scene
        # (Loading, Popup backdrop, etc.)
        self.sequences = []
        for i in args:
            self.append_layer(i)

    def draw(self):
        for layer in self.layers_coll:
            layer.draw()

    def tick(self):
        for layer in self.layers_coll:
            layer.clocked_update()

    def get(self, key):
        return self.layers_coll[self.layers[key]]

    def pause(self):
        self.get('canvas_layer').pause()

    def play(self):
        self.get('canvas_layer').play()

    def append_layer(self, layer: SceneLayer):
        layer.parent = self
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

    def on_window_resize(self, *args):
        self.get('ui_layer').on_window_resize(*args)


class Viewport():
    def __init__(self, initial_scene: Scene):
        self.scenes = []
        self.add_scene(initial_scene)
        self.resized = Event(self)

    def add_scene(self, scene: Scene):
        self.scenes.append(scene)

    @property
    def current_scene(self):
        return self.scenes[0]

    def draw(self):
        self.current_scene.draw()

    def tick(self):
        self.current_scene.tick()

    def on_window_resize(self, sender, *args):
        self.current_scene.on_window_resize(*args)
