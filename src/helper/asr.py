import threading
import qi
import argparse
import sys
import time


def status(memory_service):
    st = time.time()
    buf = time.time()
    cur = time.time()
    while cur - st < 20:
        if cur - buf >= 1:
            print("\n **{}".format(memory_service.getData("ALSpeechRecognition/Status")))
            buf = time.time()
        cur = time.time()

def main(session):
    """
    This example uses the ALSpeechRecognition module.
    """
    # Get the service ALSpeechRecognition.

    asr_service = session.service("ALSpeechRecognition")
    memory_service = session.service("ALMemory")
    

    # asr_service.removeAllContext()
    asr_service.setLanguage("English")

    # Example: Adds "yes", "no" and "please" to the vocabulary (without wordspotting)
    asr_service.pause(True)
    asr_service.removeAllContext()
    vocabulary = ["hello", "pepper", "please"]
    asr_service.setVocabulary(vocabulary, False)
    asr_service.pause(False)
    
    _status = threading.Thread(target=status, name='statuschecker', args=(memory_service,))
    _status.start()

    # Start the speech recognition engine with user Test_ASR
    asr_service.subscribe("activation")
    st = time.time()
    buf = time.time()
    cur = time.time()
    r = 0
    while cur - st < 20:
        if cur - buf >= 1:
            print(memory_service.getData("WordRecognized"))
            buf = time.time()
        cur = time.time()
        if cur - st > 10 and r == 0:
            r = 1
            memory_service.raiseEvent("WordRecognized", ["", -3.0])
    
    asr_service.pause(True)
    asr_service.removeAllContext()
    asr_service.pause(False)
    
    asr_service.unsubscribe("activation")
    
    _status.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)