from inac8hr.anim.easing import LinearEase
from inac8hr.events import Event


class SequenceInfo():
    def __init__(self, property_name, end_val, initial_val=None,
                 animation=None):
        self.start = initial_val
        self.end = end_val
        self.prop_name = property_name
        self.animation = animation


class TemporalSequence():

    def __init__(self, duration):
        self.start_behaviour = SceneSequence.TIME_CONTROLLED
        self.duration = duration
        self.started_event = Event(self)
        self.finished_event = Event(self)

    def animate(self, time):
        pass

    def end(self):
        self.on_finish()

    def on_start(self):
        self.started_event()

    def on_finish(self):
        self.finished_event()


class SceneSequence(TemporalSequence):
    """
        TODO: Sequence group
    """
    TIME_CONTROLLED = 0
    EVENT_CONTROLLED = 1

    def __init__(self, control, props: list, duration, animation=LinearEase):
        super().__init__(duration)
        self.animation = animation
        self.props = props
        self.control = control
        self.property_name = ""
        self.played = False
        self.__init_anims__()

    def __init_anims__(self):
        for prop in self.props:
            if prop.start is None:
                prop.start = getattr(self.control, prop.prop_name)
            if prop.animation is None:
                prop.animation = self.animation(start=prop.start, end=prop.end,
                                                duration=self.duration)

    def animate(self, time):
        if not self.played:
            self.played = True
            self.on_start()

        for prop in self.props:
            if prop.start is None:
                prop.start = getattr(self.control, prop.prop_name)
            setattr(self.control, prop.prop_name, prop.animation.ease(time))

    def end(self):
        for prop in self.props:
            setattr(self.control, prop.prop_name, prop.end)
        super().end()

    def on_start(self):
        self.started_event()

    def on_finish(self):
        self.finished_event()