from inac8hr.globals import *

EVENT_MAP_TEMP = {
    MOUSE_MOTION: [],
    MOUSE_PRESS: [],
    KEY_PRESS: [],
    KEY_RELEASE: []
}

class EventDispatcher():
    def __init__(self):
        self.dispatchers = []
        self.event_map = EVENT_MAP_TEMP

    def add_dispatcher(self, obj):
        self.dispatchers.append(obj)

    def register_tool_events(self):
        for t in self.dispatchers:
            for reg_event in t.registered_inputs:
                self.event_map[reg_event].append(t)

    def on_mouse_motion(self, *kwargs):
        for t in self.event_map[MOUSE_MOTION]:
            t.dispatch_mouse_motion(kwargs)