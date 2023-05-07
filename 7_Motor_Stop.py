import logging
import sys
import time
from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

# URI of the Crazyflie to connect to
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

# Default height to use for the MotionCommander
DEFAULT_HEIGHT = 0.5

# Create an event to signal when the flow deck is attached
deck_attached_event = Event()

# Configure logging to only show errors
logging.basicConfig(level=logging.ERROR)


# Define a function to handle changes to the deck flow parameter
def param_deck_flow(_, value_str):
    value = int(value_str)
    print(value)
    if value:
        # If the deck flow parameter is nonzero, signal that the deck is attached
        deck_attached_event.set()
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')


if __name__ == '__main__':
    # Initialize the Crazyflie drivers
    cflib.crtp.init_drivers()

    # Connect to the Crazyflie
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        # Register a callback for changes to the deck flow parameter
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
        # Wait for 1 second
        time.sleep(1)

        # If the deck is not attached after 5 seconds, exit the program
        if not deck_attached_event.wait(timeout=5):
            print('No flow deck detected!')
            sys.exit(1)

        # Enable the Crazyflie's motors
        scf.cf.param.set_value('motorPowerSet.enable', 1)
        # Set the motor power to zero for each motor
        scf.cf.param.set_value('motorPowerSet.m1', 0)
        scf.cf.param.set_value('motorPowerSet.m2', 0)
        scf.cf.param.set_value('motorPowerSet.m3', 0)
        scf.cf.param.set_value('motorPowerSet.m4', 0)
        # Wait
        time.sleep(0.5)
