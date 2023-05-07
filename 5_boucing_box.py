"""
Crazyflie 101 Tutorial - 5_boucing_box.py
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

# Set up logging to display error messages
logging.basicConfig(level=logging.ERROR)

# Set the URI of the Crazyflie to use
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

# Set default height and box limit
DEFAULT_HEIGHT = 0.5
BOX_LIMIT = 0.5

# Create an event to signal when the flow deck is attached
deck_attached_event = Event()

# Initialize position estimate
position_estimate = [0, 0]


# Function to move the Crazyflie within the box limit
def move_box_limit(scf):
    # Create a MotionCommander object with default height
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        # Set initial commands
        body_x_cmd = 0.2
        body_y_cmd = 0.1
        max_vel = 0.2

        # Loop until program is terminated
        while (1):
            # Check if Crazyflie is outside of box limit
            if position_estimate[0] > BOX_LIMIT:
                body_x_cmd = -max_vel
            elif position_estimate[0] < -BOX_LIMIT:
                body_x_cmd = max_vel
            if position_estimate[1] > BOX_LIMIT:
                body_y_cmd = -max_vel
            elif position_estimate[1] < -BOX_LIMIT:
                body_y_cmd = max_vel

            # Move Crazyflie linearly with updated commands
            mc.start_linear_motion(body_x_cmd, body_y_cmd, 0)

            # Sleep to allow for communication with the Crazyflie
            time.sleep(0.1)


# Function to move the Crazyflie in a simple linear pattern
def move_linear_simple(scf):
    # Create a MotionCommander object with default height
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        # Sleep to allow for communication with the Crazyflie
        time.sleep(1)
        # Move forward for 0.5 meters
        mc.forward(0.5)
        # Sleep to allow for communication with the Crazyflie
        time.sleep(1)
        # Turn left 180 degrees
        mc.turn_left(180)
        # Sleep to allow for communication with the Crazyflie
        time.sleep(1)
        # Move forward for 0.5 meters
        mc.forward(0.5)
        # Sleep to allow for communication with the Crazyflie
        time.sleep(1)


# Function to take off and hover for a short time
def take_off_simple(scf):
    # Create a MotionCommander object with default height
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        # Sleep to allow for communication with the Crazyflie
        time.sleep(3)
        # Stop moving
        mc.stop()


# This function is called when the deck parameters are updated
def param_deck_flow(_, value_str):
    value = int(value_str)
    print(value)
    if value:
        deck_attached_event.set()
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')


if __name__ == '__main__':
    # Initialize the Crazyflie drivers
    cflib.crtp.init_drivers()

    # Connect to the Crazyflie and create a SyncCrazyflie object
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

        # Add a callback for the deck parameters
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
        time.sleep(1)

        # Set up logging of the position estimate
        logconf = LogConfig(name='Position', period_in_ms=10)
        logconf.add_variable('stateEstimate.x', 'float')
        logconf.add_variable('stateEstimate.y', 'float')
        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(log_pos_callback)

        # Wait for the flow deck to be attached
        if not deck_attached_event.wait(timeout=5):
            print('No flow deck detected!')
            sys.exit(1)

        # Start logging and move the Crazyflie within the box limit
        logconf.start()
        move_box_limit(scf)
        logconf.stop()
