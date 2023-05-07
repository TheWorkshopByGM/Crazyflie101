"""
Crazyflie 101 Tutorial - 0_simple_connect.py
Author: Guy Maalouf
Date: May 12, 2023
"""

# Import required packages
import logging
import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

# URI to the Crazyflie to connect to
uri = 'radio://0/80/2M/E7E7E7E7E7'

def simple_connect():
    """
    Simple function to test connection to the Crazyflie
    """
    print("Yeah, I'm connected! :D")
    time.sleep(3)
    print("Now I will disconnect!")

if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    # Print Hello world! to console
    print("Hello world!")

    # Connect to the Crazyflie and run simple_connect() function
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        print("I'm in!")
        simple_connect()
