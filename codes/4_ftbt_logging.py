"""
Crazyflie 101 Tutorial - 4_ftbt_logging.py
Author: Guy Maalouf
Date: May 12, 2023
"""
# Import necessary libraries
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

# Define URI for the Crazyflie
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

# Define default height for the MotionCommander
DEFAULT_HEIGHT = 0.5

# Create an event to be set when a flow deck is detected
deck_attached_event = Event()

# Set up logging
logging.basicConfig(level=logging.ERROR)

# Define a list to hold position estimates
position_estimate = [0, 0]

# Define a function to make the Crazyflie move linearly
def move_linear_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(1)
        mc.forward(0.5)
        time.sleep(1)
        mc.turn_left(180)
        time.sleep(1)
        mc.forward(0.5)
        time.sleep(1)

# Define a function to make the Crazyflie take off
def take_off_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(3)
        mc.stop()

# Define a callback function for the log
def log_pos_callback(timestamp, data, logconf):
    print(data)
    global position_estimate
    position_estimate[0] = data['stateEstimate.x']
    position_estimate[1] = data['stateEstimate.y']

# Define a callback function for the parameter update
def param_deck_flow(_, value_str):
    value = int(value_str)
    print(value)
    if value:
        deck_attached_event.set() # Set the event when a flow deck is detected
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')

# Start the main program
if __name__ == '__main__':
    cflib.crtp.init_drivers() # Initialize the drivers for the Crazyflie

    # Connect to the Crazyflie
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        
        # Add a parameter update callback for the flow deck
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
        time.sleep(1)

        # Set up the log configuration for position estimates
        logconf = LogConfig(name='Position', period_in_ms=10)
        logconf.add_variable('stateEstimate.x', 'float')
        logconf.add_variable('stateEstimate.y', 'float')
        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(log_pos_callback)

        # Wait for a flow deck to be detected
        if not deck_attached_event.wait(timeout=5):
            print('No flow deck detected!')
            sys.exit(1)

        # Start the log configuration and move the Crazyflie
        logconf.start()
        move_linear_simple(scf)

        # Stop the log configuration
        logconf.stop()

