from micropython import const
import utime
import ubluetooth
import ubinascii
import struct

"""
LEGO(R) SPIKE PRIME + POWERED UP
--------------------------------

This is a basic core build on top of ubluetooth
which has the ability to detect and connect to
Powered UP devices from LEGO. Currently only the
Powered UP Remote is fully implemented and the
Control+ Hub is partially supported
"""

class PoweredUPButtons:
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


class PoweredUPColors:
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
    
class Led:
    """
    Class to control build in LED
    """
    
    def __init__(self,hub,port = 0x00):
        """
        Create a instance of LED
        """
        self.__port = port
        self.__hub = hub
        
    def __call__(self,color):
        """
        callback to control LED color

        :param color: color byte
        :returns: nothing
        """
        self.__set_led_color(color)
        
    """
    private functions
    -----------------
    """
    def __set_led_color(self, color_byte):
        color = self.__hub.__create_message([0x08, 0x00, 0x81, self.__port, 0x11, 0x51, 0x00, color_byte])
        self.__hub.__handler.write(color)

class Button:
    """
    Class to control all buttons on a hub
    """

    def __init__(self):
        """
        Create a instance of Button
        """
        pass

class SingleButton:
    """
    Class to control a single button
    """

    def __init__(self):
        """
        Create a instance of a single button
        """

        # button state
        self.__is_pressed = False
        self.__was_pressed = False
        self.__presses = 0

    def is_pressed(self):
        """
        check if button is pressed

        :returns: True if button is pressed; False if button is not pressed
        """

        return self.__is_pressed

    def was_pressed(self):
        """
        check if button was pressed since last call 

        :returns: True if button was pressed since last call; False if button was not pressed since last call
        """
        value = self.__was_pressed
        self.__was_pressed = False
        return value

    def presses(self):
        """
        Number of presses since last call

        :returns: integer value of number of presses since last call
        """ 
        value = self.__presses
        self.__presses = 0
        return value

    """
    private functions
    -----------------
    """

    def __update(self,pressed):
        """
        update button state variables

        :param pressed: boolean True if update initiated by a press on the button; False if update initiated by a release of a button
        :returns: nothing
        """

        if pressed:
            self.__presses += 1
            self.__is_pressed = True
        else:
            if self.__is_pressed:
                self.__was_pressed = True
            self.__is_pressed = False           

class RemoteButton:
    """
    Class to control button on a PoweredUP Remote
    """

    def __init__(self,hub,port):
        """
        Create a instance of a remote button
        """

        self.__port = port
        self.__hub = hub

        self.plus = SingleButton()
        self.red  = SingleButton()
        self.min  = SingleButton()

    """
    private functions
    -----------------
    """  

    def __update(self,event):
        """
        update button state variables

        :param event:  byte refering to button event
        :returns: nothing
        """

        if event == 0x01:
            self.plus.__update(True)
        elif event == 0x7F:
            self.red.__update(True)
        elif event == 0xFF:
            self.min.__update(True)
        elif event == 0x00:
            self.plus.__update(False)
            self.red.__update(False)
            self.min.__update(False)

class Motion:
    """
    Class to handle motion sensor in PoweredUP hub
    """

    def __init__(self,hub):
        """
        Create a instance of Control+ hub
        """

        self.__hub = hub

    def accelerometer(self):
        """
        acceleration around three axis 

        :returns: tuple with accleration around x,y,z axis
        """



        pass

    def gyroscope(self):
        """
        gyro rates around three axis 

        :returns: tuple with gyro rate around x,y,z axis
        """
        pass

    def yaw_pitch_roll(self):
        pass

    """
    private functions
    -----------------
    """
    def __port_value_format(self,port):
        mode = 0x00
        info_type = 0x80
        port_value_format = self.__hub.__create_message([0x06, 0x00, 0x22, port, mode, info_type])

    def __send_port_value_request(self, port):
        port_value_request = self.__hub.__create_message([0x05, 0x00, 0x21, port, 0x45])
        self.__hub.__handler.write(color)


class device():
    """
    Class to PoweredUp devices connected to a physical port
    """

    def __init__(self,hub,port):
        """
        Create a instance of Control+ hub
        """
        
        self.__hub = hub
        self.__port = port

    def mode(self, mode):
        """
        Set the mode of the sensor

        param mode: new mode
        returns: nothing
        """

        set_mode = self.__hub.__create_message([0x07, 0x00, 0x81, self.__port, 0x11, 0x51, mode])
        self.__hub.__handler.write(set_mode)
        pass

    def get(self):
        """
        Get measurement of the sensor

        returns: measurement
        """

        pass
    
class _motor:
    """
    Class to handle Motor command
    """ 

    def __init__(self,hub,port):
        self.__hub = hub
        self.__port = port

    def reset():
        pass

    def mode():
        pass

    def get():
        pass

    def pwm(power):
        pass

    def run_at_speed(speed=50, max_power=100, acceleration=100, deceleration=100, stall = False):
        pass

    def run_for_time(time, speed=50, max_power=100, acceleration=100, deceleration=100, stall=False):
        pass

    def run_for_degrees(degrees, speed=50, max_power=100, acceleration=100, deceleration=100, stop=1, stall=True):
        pass

    def run_to_position(degrees, speed=50, max_power=100, acceleration=100, deceleration=100, stop=1, stall=True):
        pass

    def coast():
        pass

    def brake():
        pass

    def hold():
        pass

    def busy(type):
        pass

    #def pair(motor):
    #    pass



class ControlPlusHub:
    """
    Class to handle LEGO(R) Control+(TM) hub
    """

    def __init__(self):
        """
        Create a instance of Control+ hub
        """
        # constants
        self.debug = False
        self.__CONTROL_PLUS_HUB_ID = 0x80
        self.__color = PoweredUPColors.BLUE
        self.__address = None

        # class specific
        self.__handler = _PoweredUPHandler()

        # callbacks
        self.__connect_callback = None
        self.__disconnect_callback = None
        
        # devices
        self.Led = Led(self,0x32)

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
        
    def is_connected(self):
        """
        Check if hub is connected
        
        :returns: nothing
        """
        return self.__handler.is_connected()

    """
    private functions
    -----------------
    """

    def __create_message(self, byte_array):
        message = struct.pack('%sb' % len(byte_array), *byte_array)
        return message

    def __on_scan(self, addr_type, addr, man_data):
        if not self.__address:
            if addr and man_data[2][1] == self.__CONTROL_PLUS_HUB_ID:
                self.__handler.connect(addr_type, addr)
        else:
            if self.__address == addr and man_data[2][1] == self.__CONTROL_PLUS_HUB_ID:
                self.__handler.connect(addr_type, addr)

    def __on_connect(self):
        #left_port = self.__create_message([0x0A, 0x00, 0x41, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01])
        #right_port = self.__create_message([0x0A, 0x00, 0x41, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01])
        #notifier = self.__create_message([0x01, 0x00])

        self.Led(self.__color)
        #utime.sleep(0.1)
        #self.__handler.write(left_port)
        #utime.sleep(0.1)
        #self.__handler.write(right_port)
        #utime.sleep(0.1)
        #self.__handler.write(notifier, 0x0C)
        if self.__connect_callback:
            self.__connect_callback()

    def __on_disconnect(self):
        if self.__disconnect_callback:
            self.__disconnect_callback()

    def __on_notify(self, data):
        print(data)
        message_type = data[3]
        port = data[4]



class PoweredUPRemote:
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
        self.__color = PoweredUPColors.BLUE
        self.__address = None


        # center button
        self.BUTTON_CENTER_GREEN = self.__create_message([0x05, 0x00, 0x08, 0x02, 0x01])
        self.BUTTON_CENTER_RELEASED = self.__create_message([0x05, 0x00, 0x08, 0x02, 0x00])

        # constants of buttons for class
        self._LEFT_BUTTON = 0
        self._RIGHT_BUTTON = 1
        self._CENTER_BUTTON = 2

        # class specific
        self.__handler = _PoweredUPHandler()

        # callbacks
        self.__connect_callback = None
        self.__disconnect_callback = None
        
        # devices
        self.led = Led(self,0x34)
        self.button = Button()
        setattr(self.button,'left', RemoteButton(self,0x00))
        setattr(self.button,'right', RemoteButton(self,0x01))
        #setattr(self.Button,'green', SingleButton())

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
        
    def is_connected(self):
        """
        Check if hub is connected
        
        :returns: nothing
        """
        return self.__handler.is_connected()

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

        self.led(self.__color)
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
        data = struct.unpack('%sB' % len(data), data)
        #data = struct.pack('%sB' % len(data_unpack), data_unpack)
        #print(data)
        message_type = data[2]
        port = data[3]

        if port == 0x00:
            self.button.left.__update(data[4])
        elif port == 0x01:
            self.button.right.__update(data[4])
        


# Internal used helper classes
# this are not for usage outside of this environment


class _PoweredUPHandler:
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
        
    def is_connected(self):
        """
        Check if hub is connected
        
        :returns: nothing
        """
        return self.__is_connected()

    """
    private functions
    -----------------
    """

    def __is_connected(self):
        return self.__conn_handle is not None and self.__value_handle is not None

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
                utime.sleep_ms(100)
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


class _Decoder:
    """
    Class to decode BLE adv_data
    """

    def __init__(self):
        """
        create instance of _Decoder
        """
        self.__COMPANY_IDENTIFIER_CODES = {"0397": "LEGO System A/S"}

    def decode_manufacturer(self, payload):
        """
        decode manufacturer information from ble data

        :param payload: payload data to decode
        :returns: nothing
        """
        man_data = []
        n = self.__decode_field(payload, const(0xFF))
        if not n:
            return []
        company_identifier = ubinascii.hexlify(struct.pack('<h', *struct.unpack('>h', n[0])))
        company_name = self.__COMPANY_IDENTIFIER_CODES.get(company_identifier.decode(), "?")
        company_data = n[0][2:]
        man_data.append(company_identifier.decode())
        man_data.append(company_name)
        man_data.append(company_data)
        return man_data

    def decode_name(self, payload):
        """
        decode name information from ble data

        :param payload: payload data to decode
        :returns: nothing
        """
        n = self.__decode_field(payload, const(0x09))
        return str(n[0], "utf-8") if n else "parsing failed!"

    def decode_services(self, payload):
        """
        decode services information from ble data

        :param payload: payload data to decode
        :returns: nothing
        """
        services = []
        for u in self.__decode_field(payload, const(0x3)):
            services.append(ubluetooth.UUID(struct.unpack("<h", u)[0]))
        for u in self.__decode_field(payload, const(0x5)):
            services.append(ubluetooth.UUID(struct.unpack("<d", u)[0]))
        for u in self.__decode_field(payload, const(0x7)):
            services.append(ubluetooth.UUID(u))
        return services

    """
    private functions
    -----------------
    """

    def __decode_field(self, payload, adv_type):
        i = 0
        result = []
        while i + 1 < len(payload):
            if payload[i + 1] == adv_type:
                result.append(payload[i + 2: i + payload[i] + 1])
            i += 1 + payload[i]
        return result

def CPhub_demo():
    
    CPhub = ControlPlusHub()
    CPhub.connect()

    while not CPhub.is_connected():
        pass

    k = 0
    while True:
        CPhub.Led(k%11)
        k+=1
        utime.sleep(1)
        
def Remote_demo():
    
    Remote = PoweredUPRemote()
    Remote.connect()

    while not Remote.is_connected():
        pass

    k = 0
    while True:
        Remote.led(k%11)
        print(Remote.button.left.red.presses())
        k+=1
        utime.sleep(1)
        
Remote_demo()