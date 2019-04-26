from inac8hr.gui import Control
from inac8hr.anim import ControlAnimator


class SceneLayer():

    def __init__(self, scene_name):
        self.name = scene_name
        self.elements = []

    def get(self, key: int):
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

    def __init__(self, scene_name, controls: list=[]):
        super().__init__(scene_name)
        self.controls = self.elements
        self.controls.extend(controls)
        self.animator = ControlAnimator()

    def register_control(self, control: Control):
        self.controls.append(control)

    def deregister_control(self, control: Control):
        self.controls.remove(control)

    def draw(self):
        for ele in self.controls:
            ele.on_draw()

    def clocked_update(self):
        for ele in self.controls:
            ele.clocked_update()
        self.animator.update()


class ToolLayer(SceneLayer):

    def __init__(self, scene_name, main_element):
        super().__init__(scene_name)
        self.elements.append(main_element)
