import argparse
import sys
import os
import qi
import naoqi

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.0.100",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--action", type=str, default="Crouch",
                        help="Robot goto posture.")
    parser.add_argument("--stiffness", type=float, default=1.0,
                        help="Motor stiffness.")
    

    args = parser.parse_args()
    session = qi.Session()
    
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
        
    store = session.service("ALStore")
    print(store.status())

    # battery_service = session.service("ALBattery")
    # print(str(battery_service.getBatteryCharge()) + "%")

    # postureService = session.service("ALRobotPosture")  
    # motionService = session.service("ALMotion")  
    # postureService.goToPosture(args.action, 0.6)
    # motionService.setStiffnesses("Body", args.stiffness)
    # postureService.stopMove()