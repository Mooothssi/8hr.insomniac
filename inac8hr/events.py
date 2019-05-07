from inac8hr.globals import UserEvent
import types


class Event():
    def __init__(self, sender):
        self.sender = sender
        self.handlers = []

    def __call__(self, *args, **kwargs):
        for handler in self.handlers:
            handler(self.sender, *args, **kwargs)

    def __iadd__(self, another: types.MethodType):
        self.handlers.append(another)
        return self

    def __isub__(self, another: types.MethodType):
        self.handlers.remove(another)
        return self


class DataClass():
    def __eq__(self, another):
        return self.__dict__ == another.__dict__

    def __hash__(self):
        return hash(str(self.__dict__))

    def __str__(self):
        return str(self.__dict__)


class Hotkey(DataClass):
    def __init__(self, key, ctrl=False, alt=False):
        self.key = key
        self.ctrl = ctrl
        self.alt = alt


class EventDispatcher():
    REGISTERED_EVENT_NAMES = {
        "mouse_motion": UserEvent.MOUSE_MOTION,
        "mouse_press": UserEvent.MOUSE_PRESS,
        "mouse_release": UserEvent.MOUSE_RELEASE,
        "key_press": UserEvent.KEY_PRESS,
        "window_resize": UserEvent.WINDOW_RESIZE
    }
    EVENTS = [UserEvent.MOUSE_MOTION, UserEvent.MOUSE_PRESS,
              UserEvent.MOUSE_RELEASE,
              UserEvent.KEY_PRESS, UserEvent.KEY_RELEASE,
              UserEvent.WINDOW_RESIZE]

    def __init__(self, manager=None):
        self.__dispatchers__ = []
        self.event_map = {}
        self.__create_event_map__(self.EVENTS)

    def __create_event_map__(self, events: list):
        for e in events:
            self.event_map[e] = []

    def add_dispatcher(self, obj):
        self.__dispatchers__.append(obj)

    def remove_dispatcher(self, dispatcher):
        self.__dispatchers__.remove(dispatcher)

    def register_dispatcher(self, obj):
        self.add_dispatcher(obj)
        for reg_event in obj.registered_inputs:
            self.event_map[reg_event].append(obj)

    def deregister_dispatcher(self, obj):
        self.remove_dispatcher(obj)
        for reg_event in obj.registered_inputs:
            self.event_map[reg_event].remove(obj)

    def register_tool_events(self):
        for t in self.__dispatchers__:
            for reg_event in t.registered_inputs:
                self.event_map[reg_event].append(t)

    def on(self, event_name, *kwargs):
        if event_name in self.REGISTERED_EVENT_NAMES:
            for t in self.event_map[self.REGISTERED_EVENT_NAMES[event_name]]:
                self.invoke(t, "on_" + event_name, *kwargs)
        else:
            print('Event has not been registered yet!')
            print(event_name)

    def invoke(self, obj, fname: str, *args):
        getattr(obj, fname)(*args)
