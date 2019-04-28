class DockStyle():
    NONE = 0
    TOP = 1 << 1
    BOTTOM = 1 << 2
    LEFT = 1 << 3
    RIGHT = 1 << 4
    FILL = 1 << 5


class AlignStyle():

    class AlignXStyle:
        NONE = 0
        LEFT = 1 << 0
        CENTER = 1 << 1
        RIGHT = 1 << 2

    class AlignYStyle:
        NONE = 0
        TOP = 1 << 3
        MIDDLE = 1 << 4
        BOTTOM = 1 << 5

    NONE = AlignXStyle.NONE | AlignYStyle.NONE
    TOP_LEFT = AlignXStyle.LEFT | AlignYStyle.TOP
    TOP_RIGHT = AlignXStyle.RIGHT | AlignYStyle.TOP
    TOP_CENTER = AlignXStyle.CENTER | AlignYStyle.TOP
    MIDDLE_CENTER = AlignXStyle.CENTER | AlignYStyle.MIDDLE
    BOTTOM_CENTER = AlignXStyle.CENTER | AlignYStyle.BOTTOM
    
