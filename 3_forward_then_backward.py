"""
Crazyflie 101 Tutorial - 3_forward_then_backward.py
Author: Guy Maalouf
Date: May 12, 2023
"""

import logging
import sys
import time
from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

# Get URI from environment variable, or use default value
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

DEFAULT_HEIGHT = 0.5

# Create an Event object to signal when the flow deck is attached
deck_attached_event = Event()

logging.basicConfig(level=logging.ERROR)

# This function moves the drone forward, turns it 180 degrees, and then moves it forward again
def move_linear_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(1)
        mc.forward(0.5)
        time.sleep(1)
        mc.turn_left(180)
        time.sleep(1)
        mc.forward(0.5)
        time.sleep(1)
        mc.turn_left(180)
        time.sleep(1)

# This function causes the drone to take off and then stop
def take_off_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(3)
        mc.stop()

# This function is called when the 'bcFlow2' parameter is updated
# It sets the deck_attached_event if the value is non-zero (indicating the flow deck is attached)
def param_deck_flow(_, value_str):
    value = int(value_str)
    print(value)
    if value:
        deck_attached_event.set()
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')

if __name__ == '__main__':
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        # Register param_deck_flow as a callback for the 'bcFlow2' parameter
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
        time.sleep(1)

        # Wait up to 5 seconds for the flow deck to be detected
        if not deck_attached_event.wait(timeout=5):
            print('No flow deck detected!')
            sys.exit(1)

        # Move the drone forward, turn it 180 degrees, and move it forward again
        move_linear_simple(scf)
