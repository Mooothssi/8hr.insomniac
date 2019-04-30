from inac8hr.gui import Point, Control, Container
from inac8hr.anim import SceneControlAnimator


class SceneLayer():

    def __init__(self, scene_name):
        self.name = scene_name
        self.elements = []
        self.parent = None

    def get_by_index(self, key: int):
        return self.elements[key]

    @property
    def main_element(self):
        return self.elements[0]

    def draw(self):
        for ele in self.elements:
            ele.draw()

    def clocked_update(self):
        for ele in self.elements:
            ele.clocked_update()


class PlayableSceneLayer(SceneLayer):

    def __init__(self, scene_name, main_element):
        super().__init__(scene_name)
        self.elements.append(main_element)

    def play(self):
        pass

    def pause(self):
        pass


class UILayer(SceneLayer):

    def __init__(self, scene_name='ui_layer', controls: list=[]):
        super().__init__(scene_name)
        self.container = Container(Point(0, 0), width=800, height=600)
        self.elements = self.container.children
        self.elements.extend(controls)
        self.animator = SceneControlAnimator()

    def register_control(self, control: Control):
        self.container.add_control(control)

    def deregister_control(self, control: Control):
        self.container.children.remove(control)

    def draw(self):
        for ele in self.elements:
            ele.on_draw()

    def clocked_update(self):
        for ele in self.elements:
            ele.tick()
        self.animator.update()

    def on_window_resize(self, *args):
        self.container.on_window_resize(*args)


class ToolLayer(SceneLayer):

    def __init__(self, scene_name, main_element):
        super().__init__(scene_name)
        self.elements.append(main_element)
