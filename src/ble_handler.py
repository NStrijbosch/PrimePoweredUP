
from micropython import const
from remote.decoder import _Decoder
import ubluetooth
# ERASE


class _BLEHandler:
    """
    Class to deal with LEGO(R) PowerUp(TM) over BLE
    """

    def __init__(self):
        """
        Create instance of _PoweredUPHandler
        """
        # constants
        self.__IRQ_SCAN_RESULT = const(1 << 4)
        self.__IRQ_SCAN_COMPLETE = const(1 << 5)
        self.__IRQ_PERIPHERAL_CONNECT = const(1 << 6)
        self.__IRQ_PERIPHERAL_DISCONNECT = const(1 << 7)
        self.__IRQ_GATTC_SERVICE_RESULT = const(1 << 8)
        self.__IRQ_GATTC_CHARACTERISTIC_RESULT = const(1 << 9)
        self.__IRQ_GATTC_READ_RESULT = const(1 << 11)
        self.__IRQ_GATTC_NOTIFY = const(1 << 13)

        self.__LEGO_SERVICE_UUID = ubluetooth.UUID("00001623-1212-EFDE-1623-785FEABCD123")
        self.__LEGO_SERVICE_CHAR = ubluetooth.UUID("00001624-1212-EFDE-1623-785FEABCD123")

        # class specific
        self.__ble = ubluetooth.BLE()
        self.__ble.active(True)
        self.__ble.irq(handler=self.__irq)
        self.__decoder = _Decoder()
        self.__reset()
        self.debug = False

        # callbacks
        self.__scan_callback = None
        self.__read_callback = None
        self.__notify_callback = None
        self.__connected_callback = None
        self.__disconnected_callback = None

    def __reset(self):
        """
        reset all necessary variables
        """
        # cached data
        self.__addr = None
        self.__addr_type = None
        self.__adv_type = None
        self.__services = None
        self.__man_data = None
        self.__name = None
        self.__conn_handle = None
        self.__value_handle = None

        # reserved callbacks
        self.__scan_callback = None
        self.__read_callback = None
        self.__notify_callback = None
        self.__connected_callback = None
        self.__disconnected_callback = None

    def __log(self, *args):
        """
        log function if debug flag is set

        :param args: arguments to log
        :returns: nothing
        """
        if not self.debug:
            return
        print(args)

    def scan_start(self, timeout, callback):
        """
        start scanning for devices

        :param timeout: timeout in ms
        :param callback: callback function, contains scan data
        :returns: nothing
        """
        self.__log("start scanning...")
        self.__scan_callback = callback
        self.__ble.gap_scan(timeout, 30000, 30000)

    def scan_stop(self):
        """
        stop scanning for devices

        :returns: nothing
        """
        self.__ble.gap_scan(None)

    def write(self, data, adv_value=None):
        """
        write data to gatt client

        :param data: data to write
        :param adv_value: advanced value to write
        :returns: nothing
        """
        if not self.__is_connected():
            return
        if adv_value:
            self.__ble.gattc_write(self.__conn_handle, adv_value, data)
        else:
            self.__ble.gattc_write(self.__conn_handle, self.__value_handle, data)

    def read(self, callback):
        """
        read data from gatt client

        :param callback: callback function, contains readed data
        :returns: nothing
        """
        if not self.__is_connected():
            return
        self.__read_callback = callback
        self.__ble.gattc_read(self.__conn_handle, self.__value_handle)

    def connect(self, addr_type, addr):
        """
        connect to a ble device

        :param addr_type: the address type of the device
        :param addr: the devices mac a binary
        :returns: nothing
        """
        self.__ble.gap_connect(addr_type, addr)

    def disconnect(self):
        """
        disconnect from a ble device

        :returns: nothing
        """
        if not self.__is_connected():
            return
        self.__ble.gap_disconnect(self.__conn_handle)

    def on_notify(self, callback):
        """
        create a callback for on notification actions

        :param callback: callback function, contains notify data
        :returns: nothing
        """
        self.__notify_callback = callback

    def on_connect(self, callback):
        """
        create a callback for on connect actions

        :param callback: callback function
        :returns: nothing
        """
        self.__connected_callback = callback

    def on_disconnect(self, callback):
        """
        create a callback for on disconnect actions

        :param callback: callback function
        :returns: nothing
        """
        self.__disconnected_callback = callback

    """
    private functions
    -----------------
    """

    def __is_connected(self):
        return self.__conn_handle is not None

    def __irq(self, event, data):
        if event == self.__IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            self.__log("result with uuid:", self.__decoder.decode_services(adv_data))
            if self.__LEGO_SERVICE_UUID in self.__decoder.decode_services(adv_data):
                self.__addr_type = addr_type
                self.__addr = bytes(addr)
                self.__adv_type = adv_type
                self.__name = self.__decoder.decode_name(adv_data)
                self.__services = self.__decoder.decode_services(adv_data)
                self.__man_data = self.__decoder.decode_manufacturer(adv_data)
                self.scan_stop()

        elif event == self.__IRQ_SCAN_COMPLETE:
            if self.__addr:
                if self.__scan_callback:
                    self.__scan_callback(self.__addr_type, self.__addr, self.__man_data)
                self.__scan_callback = None
            else:
                self.__scan_callback(None, None, None)

        elif event == self.__IRQ_PERIPHERAL_CONNECT:
            conn_handle, addr_type, addr = data
            self.__conn_handle = conn_handle
            self.__ble.gattc_discover_services(self.__conn_handle)

        elif event == self.__IRQ_PERIPHERAL_DISCONNECT:
            conn_handle, _, _ = data
            self.__disconnected_callback()
            if conn_handle == self.__conn_handle:
                self.__reset()

        elif event == self.__IRQ_GATTC_SERVICE_RESULT:
            conn_handle, start_handle, end_handle, uuid = data
            if conn_handle == self.__conn_handle and uuid == self.__LEGO_SERVICE_UUID:
                self.__ble.gattc_discover_characteristics(self.__conn_handle, start_handle, end_handle)

        elif event == self.__IRQ_GATTC_CHARACTERISTIC_RESULT:
            conn_handle, def_handle, value_handle, properties, uuid = data
            if conn_handle == self.__conn_handle and uuid == self.__LEGO_SERVICE_CHAR:
                self.__value_handle = value_handle
                self.__connected_callback()

        elif event == self.__IRQ_GATTC_READ_RESULT:
            conn_handle, value_handle, char_data = data
            if self.__read_callback:
                self.__read_callback(char_data)

        elif event == self.__IRQ_GATTC_NOTIFY:
            conn_handle, value_handle, notify_data = data
            if self.__notify_callback:
                self.__notify_callback(notify_data)