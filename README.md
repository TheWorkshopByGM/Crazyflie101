# Crazyflie 101 Tutorial
This tutorial is inspired by the official Crazyflie website with some minor modifications. The aim of this tutorial is to provide a step-by-step guide on how to control a Crazyflie drone using Python code. The tutorial is designed to be followed sequentially, with each code building on the previous one and increasing in complexity.

##Hardware Setup
To follow along with this tutorial, you will need a Crazyflie 2.0 drone with a Flowdeck mounted to it, and a Crazyradio USB module connected to your PC. The Python code runs on your PC and communicates with the drone over radio through the Crazyradio 2.0.

##Prerequisites
Before you start this tutorial, make sure you have Python 3.5 or higher installed on your system. You will also need to install the packages found in 'requirements.txt'.

##Codes explanation
Here is a brief explanation of what each code does:

Code 0 (0_simple_connect.py): This code establishes a connection between your PC and the Crazyflie drone. It is a basic check to make sure that your PC is able to communicate with the drone.

Code 1 (1_flow_deck_check.py): This code checks if the Flowdeck is connected to the drone. The Flowdeck is an add-on module that provides the drone with altitude hold, optical flow, and distance measurement capabilities. Without the Flowdeck, the drone might fly off and possibly crash or injure someone. This code ensures that the Flowdeck is connected before proceeding with the tutorial.

Code 2 (2_take_off.py): This code makes the drone take off, hover for a few seconds, and then land. It is a basic code that demonstrates how to control the drone's altitude.

Code 3 (3_ftbt.py): This code makes the drone take off, fly forward, turn 180 degrees, fly back, turn 180 degrees, and land. It demonstrates how to control the drone's pitch, roll, and yaw.

Code 4 (4_ftbt_logging.py): This code is similar to Code 3 but with the addition of logging the position estimates of the drone on the PC terminal. It demonstrates how to use the logging feature of the Crazyflie Python library.

Code 5 (5_bouncing_box.py): This code creates a virtual box within which the drone will constantly bounce off its edges until the user commands a landing. It demonstrates how to control the drone's movements within a defined space.

Code 6 (6_Motor_Control.py): This code teaches the user how to control the drone's motor speeds individually. It demonstrates how to control the drone's movements with more precision and accuracy.

Code 7 (7_Motor_Stop.py): This code is only meant to be run after Code 6 to stop all the motors from running. Once Code 6 is stopped, some motors might still be running, so this code ensures that all the motors are stopped completely.

##Running the Codes
The tutorial consists of 8 Python codes that should be run sequentially. The codes are named as follows:

0_simple_connect.py
1_flow_deck_check.py
2_take_off.py
3_ftbt.py
4_ftbt_logging.py
5_bouncing_box.py
6_Motor_Control.py
7_Motor_Stop.py

Each code in this repository builds on the previous code and adds new functionality. It is recommended that you follow the tutorial in sequence and run each code to see how the drone behavior changes with the added functionality.

#Acknowledgments
This tutorial was inspired by the official Crazyflie website's tutorials, with some minor modifications made to suit the needs of this tutorial. For a full list of tutorials, visit the [official Crazyflie website](https://www.bitcraze.io/documentation/tutorials/).

##Conclusion
This tutorial is designed to help beginners get started with controlling a Crazyflie drone using Python code. Following the tutorial sequentially and running each code should give you a good understanding of how the drone responds to different commands and how to build on the previous code to add new functionality. Good luck and happy coding!
