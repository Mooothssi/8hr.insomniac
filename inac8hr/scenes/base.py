from inac8hr.layers import SceneLayer
from inac8hr.events import Event, EventDispatcher
from inac8hr.globals import UserEvent
import arcade


class Scene():
    registered_inputs = [UserEvent.MOUSE_PRESS, UserEvent.MOUSE_RELEASE,
                         UserEvent.MOUSE_MOTION, UserEvent.KEY_PRESS]

    def __init__(self, *args: SceneLayer):
        self.layers = {}
        self.dispatcher = EventDispatcher()
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
            self.register_layer(layer)
            self.layers[layer.name] = len(self.layers_coll) - 1
    
    def register_layer(self, layer: SceneLayer):
        if layer.name == 'ui_layer':
            for ctrl in layer.elements:
                self.dispatcher.register_dispatcher(ctrl)

    def deregister_layer(self, layer: SceneLayer):
        if layer.name == 'ui_layer':
            for ctrl in layer.elements:
                self.dispatcher.deregister_dispatcher(ctrl)

    def replace_layer(self, layer: SceneLayer):
        index = self.layers[layer.name]
        self.deregister_layer(self.layers_coll[index])
        self.layers_coll.pop(index)
        self.layers_coll.insert(index, layer)
        self.register_layer(self.layers_coll[index])

    def delete_layer(self, layer_name: str):
        index = self.layers[layer_name]
        self.deregister_layer(self.layers_coll[index])
        self.layers_coll.pop(index)
        self.layers_coll.insert(index, None)

    def on_window_resize(self, *args):
        self.get('ui_layer').on_window_resize(*args)

    def on_key_press(self, key, modifiers):
        self.dispatcher.on('key_press', key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        self.dispatcher.on('mouse_press', x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.dispatcher.on('mouse_release', x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.dispatcher.on('mouse_motion', x, y, dx, dy)


class Viewport():
    def __init__(self, initial_scene: Scene, dispatcher: EventDispatcher):
        self.scenes = []
        self.__current_scene_index__ = 0
        self.add_scene(initial_scene)
        self.resized = Event(self)
        self.dispatcher = dispatcher
        self.choose_scene(0)

    def add_scene(self, scene: Scene):
        self.scenes.append(scene)

    def next_scene(self, scene: Scene):
        self.__current_scene_index__ += 1

    def choose_scene(self, index: int):
        if self.__current_scene_index__ != index:
            self.dispatcher.deregister_dispatcher(self.current_scene)
        self.__current_scene_index__ = index
        self.dispatcher.register_dispatcher(self.current_scene)

    @property
    def current_scene(self):
        return self.scenes[self.__current_scene_index__]

    def draw(self):
        self.current_scene.draw()

    def tick(self):
        self.current_scene.tick()

    def on_window_resize(self, sender, *args):
        self.current_scene.on_window_resize(*args)
