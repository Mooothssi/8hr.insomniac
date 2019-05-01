from inac8hr.layers import SceneLayer
from inac8hr.events import Event, EventDispatcher
from inac8hr.globals import UserEvent
import arcade


class Scene():
    registered_inputs = [UserEvent.MOUSE_PRESS, UserEvent.MOUSE_RELEASE,
                         UserEvent.MOUSE_MOTION, UserEvent.KEY_PRESS]

    def __init__(self, name="Scene", *args: SceneLayer):
        self.name = name
        self.layers = {}
        self.dispatcher = EventDispatcher()
        self.layers_coll = []
        self.scene_end = Event(self)
        self.scene_start = Event(self)
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

    def end_scene_and_go_to(self, next_dest_scene: str):
        self.scene_end(next_dest_scene)

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
    def __init__(self, dispatcher: EventDispatcher, initial_scene: Scene=None):
        self.scenes = {}
        self.__buffered_scene__ = None
        self.__current_scene_index__ = None
        if initial_scene is not None:
            self.add_scene(initial_scene)
        self.resized = Event(self)
        self.scene_changed = Event(self)
        self.dispatcher = dispatcher
        if initial_scene is not None:
            self.choose_scene(initial_scene.name)

    def add_scene(self, scene: Scene):
        self.scenes[scene.name] = scene

    def next_scene(self, scene: Scene):
        self.__current_scene_index__ += 1

    def choose_scene(self, index: str):
        if self.__current_scene_index__ != None and self.__current_scene_index__ != index:
            self.dispatcher.deregister_dispatcher(self.current_scene)
            self.current_scene.scene_end -= self.on_scene_changed
        self.__current_scene_index__ = index
        self.__buffered_scene__ = self.scenes[self.__current_scene_index__]
        self.dispatcher.register_dispatcher(self.current_scene)
        self.current_scene.scene_end += self.on_scene_changed

    def on_scene_changed(self, sender, *args):
        if len(args) == 1:
            self.choose_scene(args[0])

    @property
    def current_scene(self):
        return self.__get_buffered_current_scene # self.scenes[self.__current_scene_index__]
    
    @property
    def __get_buffered_current_scene(self):
        return self.__buffered_scene__

    def get(self, scene_name: str):
        return self.scenes[scene_name]

    def draw(self):
        self.current_scene.draw()

    def tick(self):
        self.current_scene.tick()

    def on_window_resize(self, sender, *args):
        for scene in self.scenes.values():
            scene.on_window_resize(*args)

