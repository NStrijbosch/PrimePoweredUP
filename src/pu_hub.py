
# create class for dealing with technic hub

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



        # class specific
        self.__handler = _BLEHandler()

        # callbacks
        self.__connect_callback = None
        self.__disconnect_callback = None

    def connect(self, timeout=3000, address=None):
        if address:
            self.__address = ubinascii.unhexlify(address.replace(':', ''))
        self.__handler.debug = self.debug
        self.__handler.on_connect(callback=self.__on_connect)
        self.__handler.on_disconnect(callback=self.__on_disconnect)
        self.__handler.on_notify(callback=self.__on_notify)
        self.__handler.scan_start(timeout, callback=self.__on_scan)

    def disconnect(self):
        self.__handler.disconnect()

    def on_connect(self, callback):
        self.__connect_callback = callback

    def on_disconnect(self, callback):
        self.__disconnect_callback = callback

    """
    private functions
    -----------------
    """

    def __create_message(self, byte_array):
        message = struct.pack('%sb' % len(byte_array), *byte_array)
        return message

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
        print(data)