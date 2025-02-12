import qi
import argparse
import sys
import numpy
from PIL import Image


def map(services):
    
    services["motion_service"].wakeUp()
    radius = 8.0
    err = services["navigation_service"].explore(radius)
    if err != 0:
        print ("Exploration failed with code {}".format(err))
        return
    
    services["navigation_service"].explore(radius)
    services["navigation_service"].stopExploration()
    
    path = services["navigation_service"].saveExploration()
    # print(path)
    print ("Exploration saved at path : {}".format(path))
    
    services["navigation_service"].startLocalization()
    services["navigation_service"].navigateToInMap([0., 0., 0.])
    services["navigation_service"].stopLocalization()

def get_map(services):
    result_map = services["navigation_service"].getMetricalMap()
    map_width = result_map[1]
    map_height = result_map[2]
    arr = numpy.array(result_map[4]).reshape(map_width, map_height)
    img = (100 - arr) * 2.55 # from 0..100 to 255..0
    img = numpy.array(img, numpy.uint8)
    Image.frombuffer('L',  (map_width, map_height), img, 'raw', 'L', 0, 1).show()
    img_f = Image.fromarray(arr)
    img_f.save("your_file.jpeg")

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
    
    if args.explore is 1: map(services)
    get_map(services)