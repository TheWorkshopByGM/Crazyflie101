"""
Crazyflie 101 Tutorial - 2_take_off.py
Author: Guy Maalouf
Date: May 12, 2023
"""

# Import necessary packages
import logging
import sys
import time
from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

# Set URI of Crazyflie to connect to
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

# Set default height for takeoff
DEFAULT_HEIGHT = 0.5

# Create event for detecting flow deck attachment
deck_attached_event = Event()

# Set logging level to ERROR
logging.basicConfig(level=logging.ERROR)


# Function for simple takeoff and landing
def take_off_simple(scf):
    # Use MotionCommander to take off, hover for 3 seconds, and then land
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(3)
        mc.stop()


# Callback function for detecting flow deck attachment
def param_deck_flow(_, value_str):
    value = int(value_str)
    print(value)
    if value:
        deck_attached_event.set()
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    # Connect to the Crazyflie
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

        # Register the param_deck_flow callback to detect flow deck attachment
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)

        # Wait for 1 second to ensure the callback is registered
        time.sleep(1)

        # If flow deck is not detected within 5 seconds, exit the program
        if not deck_attached_event.wait(timeout=5):
            print('No flow deck detected!')
            sys.exit(1)

        # If flow deck is detected, take off and land the Crazyflie
        take_off_simple(scf)
