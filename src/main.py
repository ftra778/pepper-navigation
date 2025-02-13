import argparse
import sys
import math
import pandas as pd
import os
import qi
import naoqi
import threading
import yaml
from yaml import load
import subprocess
import filters
import socket
import time
import gptpy2
from types import NoneType
from apply_motion import GestureMimicking
from speech_detection import SpeechDetection
from gptpy2.chat_server import ChatServer
from gptpy2.utils import *

## Easy copy-paste into terminal
# export PYTHONPATH=${PYTHONPATH}:/home/user1/Documents/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages

conn = None
status = True

def connect(ip, port):
    global conn
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
        print("Listening on port " + str(port) + "...")
        server.listen(1)
        conn, addr = server.accept()
        print("\nConnected to {}\n".format(addr))
    except Exception as e:
        print(e)
        return
    

def main(args, session):
    global conn
    global status
    motion_mimicking = GestureMimicking(robot=args.robot)
    speech_detector = SpeechDetection(ip=args.ip, port=args.port)
    
    # Chatbot server
    server_t = threading.Thread(target=connect, name='connect', args=("127.0.0.1", 3434))
    server_t.start()
    
    # Movement services
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")
    life_service = session.service("ALAutonomousLife")
    tracker_service = session.service("ALTracker")

    # Audio services
    tts_service = session.service("ALTextToSpeech")
    asr_service = session.service("ALSpeechRecognition")
    # asr_service.setLanguage("English")
    recorder_service = session.service("ALAudioRecorder")
    # recorder_service.stopMicrophonesRecording()
    sound_detect_service = session.service("ALSoundDetection")
    # sound_detect_service.subscribe("chatbot")
    memory_service = session.service("ALMemory")
    animation_player_service = session.service("ALAnimationPlayer")
    


    services = {    
                    "motion_service": motion_service,
                    "posture_service": posture_service,
                    "life_service": life_service,
                    "tts_service": tts_service,
                    "sound_detect_service": sound_detect_service,
                    "recorder_service": recorder_service,
                    "memory_service": memory_service,
                    "tracker_service": tracker_service,
                    "asr_service": asr_service,
                    "animation_player_service": animation_player_service
                }
    
    # # Verbose printer
    # _v_1t = None
    # _v_2t = None
    # _v_3t = None
    # print(args.verbosity)
    # if args.verbosity:
    #     if args.verbosity >= 1:
    #         def _v_1(services):
    #             global status
    #             while status:
    #                 print("* [ASR] {}".format(services["memory_service"].getData("WordRecognized")))
    #                 print("* [STATUS] {}".format(services["memory_service"].getData("ALSpeechRecognition/Status")))
    #                 print("* [SD] {}\n".format(services["memory_service"].getData("SoundDetected")))
    #                 time.sleep(3)
    #         _v_1t = threading.Thread(target=_v_1, args=(services,))
    #         _v_1t.start()
    #     if args.verbosity >= 2:
    #         def _v_2(services):
    #             global status
    #             while status:
    #                 print("* [STATUS] {}\n".format(services["memory_service"].getData("ALSpeechRecognition/Status")))
    #                 time.sleep(3)
    #         _v_2t = threading.Thread(target=_v_2, args=(services,))
    #         _v_2t.start()
    #     if args.verbosity >= 3:
    #         def _v_3(services):
    #             global status
    #             while status:
    #                 print("* [SD] {}\n".format(services["memory_service"].getData("SoundDetected")))
    #                 time.sleep(3)
    #         _v_3t = threading.Thread(target=_v_3, args=(services,))
    #         _v_3t.start()

    # services["life_service"].setAutonomousAbilityEnabled("BasicAwareness", False)
    # services["life_service"].setAutonomousAbilityEnabled("BackgroundMovement", False)
    # services["posture_service"].goToPosture("Stand", 0.8)
    
    sensitivity = 0.93
    services["sound_detect_service"].setParameter("Sensitivity", sensitivity)
    print("Sensitivity set to {}".format(sensitivity))        
    services["recorder_service"].stopMicrophonesRecording()
    services["asr_service"].setLanguage("English")

    sub_result = speech_detector.subscribe(services=services)
    if sub_result == -1:
        print("couldn't subscribe to ASR/Sound Detection, closing...")
    else:
        try:
            while True:
                speech_detector.run(services=services)                                                              # Detect speech and get audio file from pepper
                
                services["tts_service"].say("Let me think about that")
                # services["animation_player_service"].run("animations/Stand/Gestures/Hey_1")
                services["animation_player_service"].runTag("think")
                
                if conn is None:
                    print("GPT client not connected")
                    services["memory_service"].raiseEvent("WordRecognized", ["", -3.0])
                    continue
                conn.sendall((os.path.expanduser("~") + "/pepper-motion-mimicking/audio/query.wav").encode())       # Send audio file to Python 3.8 environment
                
                # Receive result from Python 3.8 environment
                buf = conn.recv(4096)
                services["posture_service"].goToPosture("Stand", 0.8)
                
                if not buf:
                    break
                result = buf.decode()
                if result == "011":
                    services["tts_service"].say("Shutting down chatbot")
                    break
                if result == "010":
                    services["tts_service"].say("I didnt catch that, could you repeat it for me?")
                    continue
                services["tts_service"].say(result)
                services["memory_service"].raiseEvent("WordRecognized", ["", -3.0])
                # services["asr_service"].pause(False)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt, closing")
    if conn is None:
        close_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        close_socket.connect(("127.0.0.1", 3434))
        while conn is None:
            pass
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        close_socket.shutdown(socket.SHUT_RDWR)
        close_socket.close()


    # motion_mimicking.read("wave")
    # motion_mimicking.apply(useWholeBody=False, services=services)
    # motion_mimicking.run(gesture="wave", useWholeBody=False, services=services)
    speech_detector.shutdown(services)
    
    status = False
    
    # if _v_1t is not None: _v_1t.join()
    # if _v_2t is not None: _v_2t.join()
    # if _v_3t is not None: _v_3t.join()
    server_t.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--robot", type=str, default="pepper",
                        help="Robot name. Leave black for pepper")
    parser.add_argument("--ip", type=str, default="localhost",
                        help="Robot IP address. Default is localhost")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number. Default is 9559")
    parser.add_argument("-name", type=str, default=r"beckon",
                        help="Name of gesture")
    parser.add_argument("--whole_body", type=bool, default=False,
                        help="Uses the whole body in the motion")
    parser.add_argument('-v', '--verbosity', action="count", 
                        help="increase output verbosity")

    args = parser.parse_args()
    if args.robot is not "dummy":
        session = qi.Session()
        try:
            session.connect("tcp://" + args.ip + ":" + str(args.port))
        except RuntimeError:
            print("Can\'t connect to {} at ip \"{}\" on port {}.\n Please check your script arguments. Run with -h option for help.".format(args.robot, args.ip, args.port))
            sys.exit(1)
        print("Connected to {}\n".format(args.robot))

    main(args, session)
    
