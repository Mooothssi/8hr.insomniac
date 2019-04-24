from inac8hr.gui.primitives import Point


class Control():
    def __init__(self, position: Point):
        self.position = position
        self.visible = True

    def on_draw(self):
        if self.visible:
            self.draw()

    def draw(self):
        pass

    def clocked_update(self):
        pass

    def show(self):
        self.visible = True
        self.on_shown()

    def on_shown(self):
        pass


class AnimatedControl(Control):
    pass
