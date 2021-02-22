from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from remote.control import PURemote, PUColors, PUButtons

"""
LEGO(R) SPIKE PRIME + POWERED UP
--------------------------------

This is a basic example:
This example let control a motor pair
with the powered up remote
"""


def on_connect():
    """
    callback on connect
    """
    hub.status_light.on("blue")


def on_disconnect():
    """
    callback on disconnect
    """
    hub.status_light.on("white")
    motor_pair.stop()


def on_button(button):
    """
    callback on button press

    :param button: button id
    """
    if button == PUButtons.RIGHT_PLUS:
        motor_pair.start(speed=75)
    elif button == PUButtons.RIGHT_MINUS:
        motor_pair.start(speed=-75)
    elif button == PUButtons.LEFT_PLUS_RIGHT_PLUS:
        motor_pair.start(steering=-45, speed=75)
    elif button == PUButtons.LEFT_MINUS_RIGHT_PLUS:
        motor_pair.start(steering=45, speed=75)
    elif button == PUButtons.LEFT_MINUS_RIGHT_MINUS:
        motor_pair.start(steering=45, speed=-75)
    elif button == PUButtons.LEFT_PLUS_RIGHT_MINUS:
        motor_pair.start(steering=-45, speed=-75)
    elif button == PUButtons.RELEASED:
        motor_pair.stop()
    else:
        motor_pair.stop()


# set up hub
hub = PrimeHub()

# set up motors
motor_pair = MotorPair('A', 'B')
motor_pair.set_stop_action('coast')

# create remote and connect
remote = PURemote()
remote.on_connect(callback=on_connect)
remote.on_disconnect(callback=on_disconnect)
remote.on_button(callback=on_button)
remote.connect()