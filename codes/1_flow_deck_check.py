"""
Crazyflie 101 Tutorial - 1_flow_deck_check.py
Author: Guy Maalouf
Date: May 12, 2023
"""

import logging
import sys
import time
from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

# Get the URI of the Crazyflie to connect to, defaulting to a URI stored in an environment variable
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

# Create an event to be set when the deck is attached to the Crazyflie
deck_attached_event = Event()

# Set up logging
logging.basicConfig(level=logging.ERROR)

# Callback function to be called when the "bcFlow2" parameter is updated
def param_deck_flow(_, value_str):
    value = int(value_str)
    print(value)
    if value:
        # If the parameter value is nonzero, set the deck_attached_event
        deck_attached_event.set()
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        # Register the param_deck_flow callback function to be called when the "bcFlow2" parameter is updated
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
        # Wait for the deck_attached_event to be set (i.e., for the deck to be attached)
        deck_attached_event.wait()
        print('Deck attached, ready to fly!')
        time.sleep(1)
