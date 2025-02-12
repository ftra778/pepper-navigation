import argparse
import sys
import os
import qi
import naoqi
import socket
import threading


current_direction = {   
                        'x': 0,
                        'y': 0,
                        'theta_z': 0
                    }

update = 0

def move(session):
    global update
    motion_service = session.service("ALMotion")
    life_service = session.service("ALAutonomousLife")
    life_service.setAutonomousAbilityEnabled("BasicAwareness", False)
    life_service.setAutonomousAbilityEnabled("BackgroundMovement", False)
    while True:
        try:
            if current_direction['x'] == "e":
                motion_service.killMove()
                return
            elif current_direction['x'] == "stop":
                motion_service.stopMove()
            elif update == 1:
                motion_service.move(current_direction['x']/5., current_direction['y']/5., current_direction['theta_z']/5.)
                print(current_direction)
                update = 0
        except KeyboardInterrupt:
            return


def listen(conn):
    global update
    while True:
        try:
            buf = conn.recv(1024)
            if not buf:
                break
            if buf == 'z':
                current_direction['x'] = "e"
                return
            elif buf == 'x':
                current_direction['x'] = "stop"
            elif buf == '^C':
                return
            elif buf == 'w' and current_direction['x'] < 5:
                current_direction['x'] = current_direction['x'] + 1
            elif buf == 's' and current_direction['x'] > -5:
                current_direction['x'] = current_direction['x'] - 1
            elif buf == 'a' and current_direction['y'] < 5:
                current_direction['y'] = current_direction['y'] + 1
            elif buf == 'd' and current_direction['y'] > -5:
                current_direction['y'] = current_direction['y'] - 1
            elif buf == 'q' and current_direction['theta_z'] < 5:
                current_direction['theta_z'] = current_direction['theta_z'] + 1
            elif buf == 'e' and current_direction['theta_z'] > -5:
                current_direction['theta_z'] = current_direction['theta_z'] - 1
            update = 1
        except KeyboardInterrupt:
            return

if __name__ == "__main__":
#     main()
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="localhost",
                        help="Server IP")
    parser.add_argument("--port", type=int, default=3366,
                        help="Server port") 
    parser.add_argument("--pepper_ip", type=str, default="localhost",
                        help="Server IP")
    parser.add_argument("--pepper_port", type=int, default=9559,
                        help="Server port") 
    args = parser.parse_args()

    IP = args.ip
    PORT = args.port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    print("Listening on port " + str(PORT) + "...")
    server.listen(1)
    conn, addr = server.accept()
    print("Connected to " + str(addr))

    session = qi.Session()
    try:
        session.connect("tcp://" + args.pepper_ip + ":" + str(args.pepper_port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.pepper_ip + "\" on port " + str(args.pepper_port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    listener = threading.Thread(target=listen, name='listener', args=(conn,))
    mover = threading.Thread(target=move, name='mover', args=(session,))

    listener.start()
    mover.start()

    listener.join()
    mover.join()

    server.close()