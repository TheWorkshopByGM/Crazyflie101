"""
Crazyflie 101 Tutorial - 6_Motor_Control.py
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

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7') # set the URI for the Crazyflie

DEFAULT_HEIGHT = 0.5

deck_attached_event = Event() # create an event to detect if the flow deck is attached
logging.basicConfig(level=logging.ERROR) # set logging level

def param_deck_flow(_, value_str):
    value = int(value_str)
    print(value)
    if value:
        deck_attached_event.set() # set the event if the flow deck is attached
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')

if __name__ == '__main__':
    cflib.crtp.init_drivers() # initialize the Crazyflie drivers

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf: # connect to the Crazyflie and create a SyncCrazyflie object

        scf.cf.param.add_update_callback(group='deck', name='bcFlow2', cb=param_deck_flow) # add a parameter update callback for the flow deck
        time.sleep(1)

        if not deck_attached_event.wait(timeout=5): # wait for the flow deck to be attached
            print('No flow deck detected!')
            sys.exit(1)

        scf.cf.param.set_value('motorPowerSet.enable',1) # enable the motor power
        while(1): # infinite loop
            scf.cf.param.set_value('motorPowerSet.m1', 3000) # set motor 1 power
            scf.cf.param.set_value('motorPowerSet.m2', 0) # set motor 2 power
            scf.cf.param.set_value('motorPowerSet.m3', 0) # set motor 3 power
            scf.cf.param.set_value('motorPowerSet.m4', 0) # set motor 4 power
            time.sleep(0.25)
            scf.cf.param.set_value('motorPowerSet.m1', 0) # set motor 1 power
            scf.cf.param.set_value('motorPowerSet.m2', 3000) # set motor 2 power
            scf.cf.param.set_value('motorPowerSet.m3', 0) # set motor 3 power
            scf.cf.param.set_value('motorPowerSet.m4', 0) # set motor 4 power
            time.sleep(0.25)
            scf.cf.param.set_value('motorPowerSet.m1', 0) # set motor 1 power
            scf.cf.param.set_value('motorPowerSet.m2', 0) # set motor 2 power
            scf.cf.param.set_value('motorPowerSet.m3', 3000) # set motor 3 power
            scf.cf.param.set_value('motorPowerSet.m4', 0) # set motor 4 power
            time.sleep(0.25)
            scf.cf.param.set_value('motorPowerSet.m1', 0) # set motor 1 power
            scf.cf.param.set_value('motorPowerSet.m2', 0) # set motor 2 power
            scf.cf.param.set_value('motorPowerSet.m3', 0) # set motor 3 power
            scf.cf.param.set_value('motorPowerSet.m4', 3000) # set motor 4 power
            time.sleep(0.25)
