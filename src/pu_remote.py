
from remote.constants import PUButtons, PUColors
from remote.ble_handler import _BLEHandler
from remote.decoder import _Decoder
import ubinascii
# ERASE

"""
LEGO(R) SPIKE PRIME + POWERED UP
--------------------------------

This is a basic core build on top of ubluetooth
which has the ability to detect and connect to
Powered UP devices from Lego. Currently only the
Powered UP Remote is fully implemented.
"""


class PURemote:
    """
    Class to handle LEGO(R) PowerUP(TM) Remote
    """

    def __init__(self):
        """
        Create a instance of PowerUP Remote
        """
        # constants
        self.debug = False
        self.__POWERED_UP_REMOTE_ID = 66
        self.__color = PUColors.BLUE
        self.__address = None

        # left buttons
        self.BUTTON_LEFT_PLUS = self.__create_message([0x05, 0x00, 0x45, 0x00, 0x01])
        self.BUTTON_LEFT_RED = self.__create_message([0x05, 0x00, 0x45, 0x00, 0x7F])
        self.BUTTON_LEFT_MINUS = self.__create_message([0x05, 0x00, 0x45, 0x00, 0xFF])
        self.BUTTON_LEFT_RELEASED = self.__create_message([0x05, 0x00, 0x45, 0x00, 0x00])

        # right buttons
        self.BUTTON_RIGHT_PLUS = self.__create_message([0x05, 0x00, 0x45, 0x01, 0x01])
        self.BUTTON_RIGHT_RED = self.__create_message([0x05, 0x00, 0x45, 0x01, 0x7F])
        self.BUTTON_RIGHT_MINUS = self.__create_message([0x05, 0x00, 0x45, 0x01, 0xFF])
        self.BUTTON_RIGHT_RELEASED = self.__create_message([0x05, 0x00, 0x45, 0x01, 0x00])

        # center button
        self.BUTTON_CENTER_GREEN = self.__create_message([0x05, 0x00, 0x08, 0x02, 0x01])
        self.BUTTON_CENTER_RELEASED = self.__create_message([0x05, 0x00, 0x08, 0x02, 0x00])

        # constants of buttons for class
        self._LEFT_BUTTON = 0
        self._RIGHT_BUTTON = 1
        self._CENTER_BUTTON = 2

        # class specific
        self.__handler = _BLEHandler()
        self.__buttons = [self.BUTTON_LEFT_RELEASED, self.BUTTON_RIGHT_RELEASED, self.BUTTON_CENTER_RELEASED]

        # callbacks
        self.__button_callback = None
        self.__connect_callback = None
        self.__disconnect_callback = None

    def connect(self, timeout=3000, address=None):
        """
        connect to a powered up remote

        :param timeout: time of scanning for devices in ms, default is 3000
        :param address: mac address of device, connect to a specific device if set
        :returns: nothing
        """
        if address:
            self.__address = ubinascii.unhexlify(address.replace(':', ''))
        self.__handler.debug = self.debug
        self.__handler.on_connect(callback=self.__on_connect)
        self.__handler.on_disconnect(callback=self.__on_disconnect)
        self.__handler.on_notify(callback=self.__on_notify)
        self.__handler.scan_start(timeout, callback=self.__on_scan)

    def disconnect(self):
        """
        disconnect from a powered up remote
        :returns: nothing
        """
        self.__handler.disconnect()

    def set_color(self, color):
        """
        set color of a connected remote, use PoweredUPColors class

        :param color: color byte
        :returns: nothing
        """
        self.__set_remote_color(color)

    def on_button(self, callback):
        """
        create a callback for button actions

        :param callback: callback function, contains button data
        :returns: nothing
        """
        self.__button_callback = callback

    def on_connect(self, callback):
        """
        create a callback for on connect actions

        :param callback: callback function
        :returns: nothing
        """
        self.__connect_callback = callback

    def on_disconnect(self, callback):
        """
        create a callback for on disconnect actions

        :param callback: callback function
        :returns: nothing
        """
        self.__disconnect_callback = callback

    """
    private functions
    -----------------
    """

    def __create_message(self, byte_array):
        message = struct.pack('%sb' % len(byte_array), *byte_array)
        return message

    def __set_remote_color(self, color_byte):
        color = self.__create_message([0x08, 0x00, 0x81, 0x34, 0x11, 0x51, 0x00, color_byte])
        self.__handler.write(color)

    def __on_scan(self, addr_type, addr, man_data):
        if not self.__address:
            if addr and man_data[2][1] == self.__POWERED_UP_REMOTE_ID:
                self.__handler.connect(addr_type, addr)
        else:
            if self.__address == addr and man_data[2][1] == self.__POWERED_UP_REMOTE_ID:
                self.__handler.connect(addr_type, addr)

    def __on_connect(self):
        left_port = self.__create_message([0x0A, 0x00, 0x41, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01])
        right_port = self.__create_message([0x0A, 0x00, 0x41, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01])
        notifier = self.__create_message([0x01, 0x00])

        self.__set_remote_color(self.__color)
        utime.sleep(0.1)
        self.__handler.write(left_port)
        utime.sleep(0.1)
        self.__handler.write(right_port)
        utime.sleep(0.1)
        self.__handler.write(notifier, 0x0C)
        if self.__connect_callback:
            self.__connect_callback()

    def __on_disconnect(self):
        if self.__disconnect_callback:
            self.__disconnect_callback()

    def __on_notify(self, data):
        if data == self.BUTTON_LEFT_PLUS:
            self.__buttons[self._LEFT_BUTTON] = self.BUTTON_LEFT_PLUS
        if data == self.BUTTON_LEFT_RED:
            self.__buttons[self._LEFT_BUTTON] = self.BUTTON_LEFT_RED
        if data == self.BUTTON_LEFT_MINUS:
            self.__buttons[self._LEFT_BUTTON] = self.BUTTON_LEFT_MINUS
        if data == self.BUTTON_LEFT_RELEASED:
            self.__buttons[self._LEFT_BUTTON] = self.BUTTON_LEFT_RELEASED
        if data == self.BUTTON_RIGHT_PLUS:
            self.__buttons[self._RIGHT_BUTTON] = self.BUTTON_RIGHT_PLUS
        if data == self.BUTTON_RIGHT_RED:
            self.__buttons[self._RIGHT_BUTTON] = self.BUTTON_RIGHT_RED
        if data == self.BUTTON_RIGHT_MINUS:
            self.__buttons[self._RIGHT_BUTTON] = self.BUTTON_RIGHT_MINUS
        if data == self.BUTTON_RIGHT_RELEASED:
            self.__buttons[self._RIGHT_BUTTON] = self.BUTTON_RIGHT_RELEASED
        if data == self.BUTTON_CENTER_GREEN:
            self.__buttons[self._CENTER_BUTTON] = self.BUTTON_CENTER_GREEN
        if data == self.BUTTON_CENTER_RELEASED:
            self.__buttons[self._CENTER_BUTTON] = self.BUTTON_CENTER_RELEASED

        self.__on_button(self.__buttons)

    def __on_button(self, buttons):
        if buttons[self._LEFT_BUTTON] == self.BUTTON_LEFT_RELEASED and buttons[self._RIGHT_BUTTON] == self.BUTTON_RIGHT_RELEASED and buttons[self._CENTER_BUTTON] == self.BUTTON_CENTER_RELEASED:
            button = PUButtons.RELEASED
        elif buttons[self._LEFT_BUTTON] == self.BUTTON_LEFT_PLUS and buttons[self._RIGHT_BUTTON] == self.BUTTON_RIGHT_RELEASED and buttons[self._CENTER_BUTTON] == self.BUTTON_CENTER_RELEASED:
            button = PUButtons.LEFT_PLUS
        elif buttons[self._LEFT_BUTTON] == self.BUTTON_LEFT_RED and buttons[self._RIGHT_BUTTON] == self.BUTTON_RIGHT_RELEASED and buttons[self._CENTER_BUTTON] == self.BUTTON_CENTER_RELEASED:
            button = PUButtons.LEFT_RED
        elif buttons[self._LEFT_BUTTON] == self.BUTTON_LEFT_MINUS and buttons[self._RIGHT_BUTTON] == self.BUTTON_RIGHT_RELEASED and buttons[self._CENTER_BUTTON] == self.BUTTON_CENTER_RELEASED:
            button = PUButtons.LEFT_MINUS
        elif buttons[self._RIGHT_BUTTON] == self.BUTTON_RIGHT_PLUS and buttons[self._LEFT_BUTTON] == self.BUTTON_LEFT_RELEASED and buttons[self._CENTER_BUTTON] == self.BUTTON_CENTER_RELEASED:
            button = PUButtons.RIGHT_PLUS
        elif buttons[self._RIGHT_BUTTON] == self.BUTTON_RIGHT_RED and buttons[self._LEFT_BUTTON] == self.BUTTON_LEFT_RELEASED and buttons[self._CENTER_BUTTON] == self.BUTTON_CENTER_RELEASED:
            button = PUButtons.RIGHT_RED
        elif buttons[self._RIGHT_BUTTON] == self.BUTTON_RIGHT_MINUS and buttons[self._LEFT_BUTTON] == self.BUTTON_LEFT_RELEASED and buttons[self._CENTER_BUTTON] == self.BUTTON_CENTER_RELEASED:
            button = PUButtons.RIGHT_MINUS
        elif buttons[self._LEFT_BUTTON] == self.BUTTON_LEFT_PLUS and buttons[self._RIGHT_BUTTON] == self.BUTTON_RIGHT_PLUS and buttons[self._CENTER_BUTTON] == self.BUTTON_CENTER_RELEASED:
            button = PUButtons.LEFT_PLUS_RIGHT_PLUS
        elif buttons[self._LEFT_BUTTON] == self.BUTTON_LEFT_MINUS and buttons[self._RIGHT_BUTTON] == self.BUTTON_RIGHT_MINUS and buttons[self._CENTER_BUTTON] == self.BUTTON_CENTER_RELEASED:
            button = PUButtons.LEFT_MINUS_RIGHT_MINUS
        elif buttons[self._LEFT_BUTTON] == self.BUTTON_LEFT_PLUS and buttons[self._RIGHT_BUTTON] == self.BUTTON_RIGHT_MINUS and buttons[self._CENTER_BUTTON] == self.BUTTON_CENTER_RELEASED:
            button = PUButtons.LEFT_PLUS_RIGHT_MINUS
        elif buttons[self._LEFT_BUTTON] == self.BUTTON_LEFT_MINUS and buttons[self._RIGHT_BUTTON] == self.BUTTON_RIGHT_PLUS and buttons[self._CENTER_BUTTON] == self.BUTTON_CENTER_RELEASED:
            button = PUButtons.LEFT_MINUS_RIGHT_PLUS
        elif buttons[self._CENTER_BUTTON] == self.BUTTON_CENTER_GREEN and buttons[self._LEFT_BUTTON] == self.BUTTON_LEFT_RELEASED and buttons[self._RIGHT_BUTTON] == self.BUTTON_RIGHT_RELEASED:
            button = PUButtons.CENTER
        else:
            button = PUButtons.RELEASED

        # callback the button data
        if self.__button_callback:
            self.__button_callback(button)