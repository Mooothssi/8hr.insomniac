from inac8hr.anim.easing import LinearEase
from inac8hr.anim.base import AnimFX, AnimFXPrefabs, AnimProperty
from inac8hr.events import Event


class ControlSequenceGroup():
    def __init__(self, duration):
        self.duration = duration
        self.sequences = []

    def add_sequence(self, info):
        self.sequences.append(info)

    def animate(self, time):
        for seq in self.sequences:
            seq.animate(time)

    def end(self):
        for seq in self.sequences:
            seq.animate(self.duration)

    @property
    def last_sequence(self):
        return self.sequences[-1]


class ControlSequence():
    AFTER_PREVIOUS = 0
    WITH_PREVIOUS = 1

    def __init__(self, control, duration, effect: AnimFX=AnimFXPrefabs.NONE):
        self.duration = duration
        self.sequences = []
        self.effects = [effect]
        self.timing_start = ControlSequence.AFTER_PREVIOUS
        self.played = False
        self.control = control
        self.__init_anims__()

    def __init_anims__(self):
        for effect in self.effects:
            self.__reset_easing__(effect)

    def __reset_easing__(self, effect):
        effect.easing_fn.start = AnimProperty.get_prop(self.control,
                                                       effect.properties)
        effect.easing_fn.duration = self.duration

    def add_effect(self, effect):
        self.sequences.append(effect)
        self.__reset_easing__(effect)

    def animate(self, time):
        for effect in self.effects:
            effect.animate(self.control, time)


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