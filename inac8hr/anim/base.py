from enum import Flag, Enum
from inac8hr.anim.easing import EasingBase, LinearEase


class AnimProperty:
    NONE = 0
    PositionX = 1
    PositionY = 2
    Opacity = 4
    Width = 8
    Height = 16
    Position = PositionX | PositionY
    PROPS = [NONE, PositionX, PositionY, Opacity, Position, Width, Height]
    NAMES = {
        Opacity: "opacity",
        PositionX: "position.x",
        PositionY: "position.y",
        Width: "width",
        Height: "height"
    }

#
# Getters & setters
#

    @staticmethod
    def get_prop(obj, prop: int):
        lst = AnimProperty.NAMES[prop].split(".")
        if len(lst) == 1:
            return getattr(obj, lst[0])
        else:
            return AnimProperty.get_prop(obj, prop)

    @staticmethod
    def set_prop(obj, prop: int, value):
        lst = AnimProperty.NAMES[prop].split(".")
        if len(lst) == 1:
            setattr(obj, lst[0], value)
        else:
            AnimProperty.set_prop(obj, prop, value)

#
#
#


class AnimAppearanceBehaviour(Enum):
    NONE = 0
    ENTRANCE = 1
    EXIT = 2


class AnimFX():

    def __init__(self, int_val, properties: int,
                 appearance: AnimAppearanceBehaviour=AnimAppearanceBehaviour.NONE,
                 end_val: int=1,
                 easing_fn: EasingBase=LinearEase):
        self._int_val = int_val
        self.properties = properties
        self.appearance = appearance
        self.endpoints = (0, end_val)
        self._easing_fn = easing_fn()
        self._easing_fn.start = self.endpoints[0]
        self._init_easing()

    def _init_easing(self):
        if self.appearance == AnimAppearanceBehaviour.EXIT:
            self._easing_fn.end = 0
        else:
            self._easing_fn.end = self.endpoints[1]

    def animate(self, control, time):
        animated_props = [prop for prop in AnimProperty.PROPS
                          if self.properties & prop]
        for prop in animated_props:
            AnimProperty.set_prop(control, prop,
                                  self._easing_fn.ease(time))

    def get_easing(self):
        return self._easing_fn

    def set_easing(self, value):
        self._easing_fn = value

    easing_fn = property(get_easing, set_easing)

    def __or__(self, another):
        obj = AnimFXPrefabs.NONE
        obj.intvalue = self._int_val | another._int_val
        return obj

    def __and__(self, another):
        return self._int_val & another._int_val


class AnimFXPrefabs:
    NONE = AnimFX(0, AnimProperty.NONE, AnimAppearanceBehaviour.NONE)
    FadeIn = AnimFX(1, AnimProperty.Opacity,
                    AnimAppearanceBehaviour.ENTRANCE, 255)
    FadeInTooltip = AnimFX(1, AnimProperty.Opacity,
                           AnimAppearanceBehaviour.ENTRANCE, 190)
    FadeOut = AnimFX(2, AnimProperty.Opacity, AnimAppearanceBehaviour.EXIT)
