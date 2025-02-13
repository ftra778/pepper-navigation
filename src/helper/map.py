import qi
import argparse
import sys
import numpy
import time
from PIL import Image


def map(services):
    
    services["motion_service"].wakeUp()
    radius = 10.0
    err = services["navigation_service"].explore(radius)
    if err != 0:
        print ("Exploration failed with code {}".format(err))
        return
    else:
        print("Exploration success: {}".format(err))
    
    services["navigation_service"].stopExploration()
    
    path = services["navigation_service"].saveExploration()
    print(path)
    print ("Exploration saved at path : {}".format(path))
    
    services["navigation_service"].startLocalization()
    services["navigation_service"].navigateToInMap([0., 0., 0.])
    services["navigation_service"].stopLocalization()

def get_map(services):
    services["navigation_service"].loadExploration("/home/nao/.local/share/Explorer/2025-02-13T002705.781Z.explo")
    # services["navigation_service"].stopLocalization()
    result_map = services["navigation_service"].getMetricalMap()
    map_width = result_map[1]
    map_height = result_map[2]
    arr = numpy.array(result_map[4]).reshape(map_width, map_height)
    img = (100 - arr) * 2.55 # from 0..100 to 255..0
    img = numpy.array(img, numpy.uint8)
    Image.frombuffer('L',  (map_width, map_height), img, 'raw', 'L', 0, 1).show()        
    # zz=numpy.asarray(img)
    # print(zz.max(), zz.min(), zz.dtype, zz.shape) # Verify something has been read
    # x = input("Pause")
    
def nav(services):
    services["navigation_service"].loadExploration("/home/nao/.local/share/Explorer/2025-02-13T002705.781Z.explo")
    services["navigation_service"].startLocalization()
    
    # services["navigation_service"].stopLocalization()
    
def move(services, x, y, z):
    services["navigation_service"].navigateToInMap([x, y, z])
    
def get(services):
    print(services["navigation_service"].getRobotPositionInMap())
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--explore", type=int, default=0,
                        help="Let Pepper explore. Default is 0 (False)")
    

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
            "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    
    
    navigation_service = session.service("ALNavigation")
    motion_service = session.service("ALMotion")
    
    services = {    
                    "navigation_service": navigation_service,
                    "motion_service": motion_service
                }
    
    # Must be number between 0.0 - 1.0?
    # move(services, 0.0, 0.0, 0.0)
    # get(services)
    # time.sleep(2)
    # move(services, 0.5, 0.0, 0.0)
    # get(services)
    # time.sleep(2)
    # move(services, 0.5, 0.5, 0.0)
    # get(services)
    # time.sleep(2)
    # move(services, 0.0, 0.5, 0.0)
    # get(services)
    # time.sleep(2)
    # move(services, 0.0, 0.5, 0.5)
    # get(services)
    # time.sleep(2)
    # move(services, 0.0, 0.0, 0.5)
    # get(services)
    # time.sleep(2)
    # move(services, 0.5, 0.0, 0.5)
    # get(services)
    # time.sleep(2)
    # move(services, 0.0, 0.0, 0.0)
    # get(services)
    # nav(services)
    # if args.explore is 1: map(services)
    get_map(services)