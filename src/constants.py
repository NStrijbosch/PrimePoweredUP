
from micropython import const
# ERASE


class PUButtons:
    """
    LEGO(R) PowerUP(TM) Button Constants
    """

    def __init__(self):
        pass

    RELEASED = const(0x00)
    LEFT_PLUS = const(0x01)
    LEFT_RED = const(0x02)
    LEFT_MINUS = const(0x03)
    RIGHT_PLUS = const(0x04)
    RIGHT_RED = const(0x05)
    RIGHT_MINUS = const(0x06)
    LEFT_PLUS_RIGHT_PLUS = const(0x07)
    LEFT_MINUS_RIGHT_MINUS = const(0x08)
    LEFT_PLUS_RIGHT_MINUS = const(0x09)
    LEFT_MINUS_RIGHT_PLUS = const(0x0A)
    CENTER = const(0x0B)


class PUColors:
    """LEGO(R) PowerUP()TM Colors"""

    def __init__(self):
        pass

    OFF = const(0x00)
    PINK = const(0x01)
    PURPLE = const(0x02)
    BLUE = const(0x03)
    LIGHTBLUE = const(0x04)
    LIGHTGREEN = const(0x05)
    GREEN = const(0x06)
    YELLOW = const(0x07)
    ORANGE = const(0x08)
    RED = const(0x09)
    WHITE = const(0x0A)