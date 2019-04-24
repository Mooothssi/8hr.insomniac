from inac8hr.gui.controls.base import Control, AnimatedControl


class ScrollablePaneView(Control):

    def __init__(self):
        self.__items__ = []

    @property
    def items(self):
        return self.__items__
