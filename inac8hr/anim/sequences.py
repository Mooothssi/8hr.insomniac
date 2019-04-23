from inac8hr.anim.easing import LinearEase


class SequenceInfo():
    def __init__(self, property_name, end_val, initial_val=None,
                 animation=None):
        self.start = initial_val
        self.end = end_val
        self.prop_name = property_name
        self.animation = animation


class SceneSequence():
    """
        TODO: Sequence group
    """
    TIME_CONTROLLED = 0
    EVENT_CONTROLLED = 1

    def __init__(self, control, props: list, duration, animation=LinearEase):
        self.animation = animation
        self.props = props
        self.control = control
        self.duration = duration
        self.property_name = ""
        self.played = False
        self.start_behaviour = SceneSequence.TIME_CONTROLLED
        self.__init_anims__()

    def __init_anims__(self):
        for prop in self.props:
            if prop.start is None:
                prop.start = getattr(self.control, prop.prop_name)
            if prop.animation is None:
                prop.animation = self.animation(start=prop.start, end=prop.end,
                                                duration=self.duration)

    def animate(self, time):
        for prop in self.props:
            setattr(self.control, prop.prop_name, prop.animation.ease(time))
