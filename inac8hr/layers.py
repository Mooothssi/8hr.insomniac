class SceneLayer():

    def __init__(self, scene_name):
        self.name = scene_name
        self.main_element = None

    def draw(self):
        if self.main_element is not None:
            self.main_element.draw()

    def clocked_update(self):
        if self.main_element is not None:
            self.main_element.clocked_update()


class PlayableSceneLayer(SceneLayer):

    def __init__(self, scene_name, main_element):
        super().__init__(scene_name)
        self.main_element = main_element

    def play(self):
        pass

    def pause(self):
        pass


class ToolLayer(SceneLayer):

    def __init__(self, scene_name, main_element):
        super().__init__(scene_name)
        self.main_element = []

    def draw(self):
        if self.main_element is not None:
            for tool in self.main_element:
                tool.draw()

    def clocked_update(self):
        if self.main_element is not None:
            for tool in self.main_element:
                tool.clocked_update()