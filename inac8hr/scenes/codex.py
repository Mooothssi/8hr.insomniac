from inac8hr.scenes import Scene
from inac8hr.hud import CodexLayer


class CodexScene(Scene):
    def __init__(self):
        super().__init__("CodexScene")
        self.append_layer(CodexLayer())
