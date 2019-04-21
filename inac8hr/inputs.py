from inac8hr.globals import *


class EventDispatcher():
    REGISTERED_EVENT_NAMES = {
        "mouse_motion": MOUSE_MOTION,
        "mouse_press": MOUSE_PRESS
    }
    EVENTS = [MOUSE_MOTION, MOUSE_PRESS,
              KEY_PRESS, KEY_RELEASE,
              WINDOW_RESIZE]

    def __init__(self):
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
                self.invoke(t, "on_" + event_name, kwargs)
        else:
            print('Event has not been registered yet!')

    def on_resize(self, *kwargs):
        for t in self.event_map[WINDOW_RESIZE]:
            t.on_resize()

    def invoke(self, obj, fname: str, args: tuple):
        getattr(obj, fname)(args)
