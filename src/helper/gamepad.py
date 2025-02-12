#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file presents an interface for interacting with the Playstation 4 Controller
# in Python. Simply plug your PS4 controller into your computer using USB and run this
# script!
#
# NOTE: I assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# Copyright © 2015 Clay L. McLeod <clay.l.mcleod@gmail.com>
#
# Distributed under terms of the MIT license.
import os
import sys
import time
import pygame
import argparse
import qi
import numpy
import threading
from PIL import Image

class EmergencyException(Exception):
    pass

class StopException(Exception):
    pass

class Keyboard():
    # TODO
    def __init__(self):
        pygame.init()
    
    
    def listen():
        try:
            while True:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            print("Left")
                        if event.key == pygame.K_RIGHT:
                            print("Right")
        except KeyboardInterrupt:
            print("KeyboardInterrupt")


class PS4Controller(object):

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""
        
        self.motion_service = session.service("ALMotion")
        
        posture_service = session.service("ALRobotPosture")
        posture_service.goToPosture("Stand", 0.8)
        
        life_service = session.service("ALAutonomousLife")
        life_service.setAutonomousAbilityEnabled("BasicAwareness", False)
        life_service.setAutonomousAbilityEnabled("BackgroundMovement", False)
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.axis_data = {}
        self.axis_data[0] = 0
        self.axis_data[1] = 0
        self.axis_data[2] = 0
        
        self.stopped = False
        
        self.speed = 1
        self.x = 0
        self.y = 0
        self.z = 0


    def listen(self, 
            #    session
               ):
        """Listen for events to happen"""
        
        try:
            if not self.axis_data:
                self.axis_data = {}

            if not self.button_data:
                self.button_data = {}
                for i in range(self.controller.get_numbuttons()):
                    self.button_data[i] = False

            if not self.hat_data:
                self.hat_data = {}
                for i in range(self.controller.get_numhats()):
                    self.hat_data[i] = (0, 0)

            speed_change = False
            buffer = time.time()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                        self.axis_data[event.axis] = round(event.value,2)
                    elif event.type == pygame.JOYBUTTONDOWN:
                        self.button_data[event.button] = True
                    elif event.type == pygame.JOYBUTTONUP:
                        self.button_data[event.button] = False
                    elif event.type == pygame.JOYHATMOTION:
                        self.hat_data[event.hat] = event.value

                    # Log most recent events
                    if speed_change is False:
                        if self.hat_data[0][1] == 1 and round(self.speed, 1) < 2:
                            speed_change = True
                            self.speed = self.speed + 0.1
                        if self.hat_data[0][1] == -1 and round(self.speed, 1) > 0.5:
                            speed_change = True
                            self.speed = self.speed - 0.1

                    if self.hat_data[0][1] == 0:
                        speed_change = False  

                    
                    # os.system('clear')
                    if self.button_data[2] == 1:
                        raise EmergencyException()

                    if self.button_data[1] == 1:
                        raise StopException

                    os.system('clear')
                    print("Speed: {}".format(self.speed))
                    if self.axis_data[0] > 0.3:
                        self.y = -1 * self.axis_data[0]
                        print("Right: {}".format(-1 * self.y))
                    elif self.axis_data[0] < -0.3:
                        self.y = -1 * self.axis_data[0]
                        pass
                        print("Left: {}".format(self.y))
                    else:
                        self.y = 0
                        print("Stationary: {}".format(self.y))

                    if self.axis_data[1] > 0.3:
                        self.x = -1 * self.axis_data[1]
                        pass
                        print("Backwards: {}".format(-1 * self.x))
                    elif self.axis_data[1] < -0.3:
                        self.x = -1 * self.axis_data[1]
                        pass
                        print("Forwards: {}".format(self.x))
                    else:
                        self.axis_data[1] = 0
                        self.x = 0
                        print("Stationary: {}".format(self.x))

                    if self.axis_data[2] > 0.3:
                        self.z = -1 * self.axis_data[2]
                        pass
                        print("Pan Right: {}".format(-1 * self.z))
                    elif self.axis_data[2] < -0.3:
                        self.z = -1 * self.axis_data[2]
                        pass
                        print("Pan Left: {}".format(self.z))
                    else:
                        self.z = 0
                        print("Stationary: {}".format(self.z))
                    
                    
        except EmergencyException:
            self.motion_service.killMove()
            print("Emergency Exit")
            
        except StopException:
            print("Stopped")
            
        self.stopped = True


def move(control):
    buffer = time.time()
    while True:
        if (time.time() - buffer > 0.05):
            control.motion_service.move(round((control.x/2.) * control.speed, 2), 
                                        round((control.y/2.) * control.speed, 2), 
                                        round((control.z/2.) * control.speed, 2))
            buffer = time.time()
        elif(control.stopped is True):
            control.motion_service.stopMove()
            break
                

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="localhost",
                        help="Robot IP address. Default is localhost")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number. Default is 9559")
    args = parser.parse_args()

    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    # key = Keyboard()
    
    ps4 = PS4Controller()
    ps4.init()
    
    controller_t = threading.Thread(target=ps4.listen, name='listen')
    move_t = threading.Thread(target=move, name='move', args=(ps4,))
    
    controller_t.start()
    move_t.start()
    
    controller_t.join()
    move_t.join()

