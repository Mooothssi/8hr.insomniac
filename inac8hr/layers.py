from inac8hr.gui import Control


class SceneLayer():

    def __init__(self, scene_name):
        self.name = scene_name
        self.main_elements = []

    @property
    def main_element(self):
        return self.main_elements[0]

    def draw(self):
        for ele in self.main_elements:
            ele.draw()

    def clocked_update(self):
        for ele in self.main_elements:
            ele.clocked_update()


class PlayableSceneLayer(SceneLayer):

    def __init__(self, scene_name, main_element):
        super().__init__(scene_name)
        self.main_elements.append(main_element)

    def play(self):
        pass

    def pause(self):
        pass


class UILayer(SceneLayer):

    def __init__(self, scene_name, controls: list=[]):
        super().__init__(scene_name)
        self.controls = self.main_elements
        self.controls.extend(controls)

    def register_control(self, control: Control):
        self.controls.append(control)

    def deregister_control(self, control: Control):
        self.controls.remove(control)


class ToolLayer(SceneLayer):

    def __init__(self, scene_name, main_element):
        super().__init__(scene_name)
        self.main_elements.append(main_element)