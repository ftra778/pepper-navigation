import qi
import argparse
import sys
import time
import subprocess
import socket
import select
import threading
import os
import requests
from types import NoneType
from gptpy2.chat_server import ChatServer



class SpeechDetection():
    def __init__(self, ip, port, format="wav", rate=44100, audio_path=None):
            
        self.AI_SERVER = "http://192.168.0.102:8000"
        self.client = None
        self.format = format
        self.rate = rate
        self.nao_path = "/home/nao/query.{}".format(format)
        self.nao_ip = ip
        self.nao_port = port
        if audio_path is None:
            self.audio_path = os.path.expanduser("~") + r"/pepper-motion-mimicking/audio/"
        else:
            self.audio_path = audio_path

    def transcribe_audio(self, audio_file):
        """ Sends audio file to AI server for transcription """
        try:
            files = {'audio': open(audio_file, 'rb')}
            response = requests.post(self.AI_SERVER + "/transcribe", files=files)
            return response.json()
        except Exception as e:
            print("Error in transcription:", e)
            return None

    def generate_response(self, text):
        """ Sends transcribed text to AI server and gets response """
        try:
            response = requests.post(self.AI_SERVER + "/generate", json={"text": text})
            return response.json()
        except Exception as e:
            print("Error in AI response:", e)
            return None
    def connect(self, ip="127.0.0.1", port=3434):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))
        print("Connected to {}:{}".format(ip, port))
        
    # Send audio data over socket
    def send(self, sock=None, content="/home/user1/nao/query.wav"):
        if sock is None:
            sock = self.client
        sock.sendall(content.encode())
    
    def subscribe(self, services):
        vocabulary = ["hello", "pepper"]
        services["asr_service"].pause(True)
        retry = 0
        while retry < 6:
            try:
                services["asr_service"].pause(True)
                services["asr_service"].removeAllContext()
                services["asr_service"].setVocabulary(vocabulary, False)
                break
            except RuntimeError as e:
                print("{} exception: Retrying in 5 seconds...".format(e))
                retry = retry + 1
                time.sleep(5)
                continue
        if retry >= 5:
            services["asr_service"].pause(False)
            return -1
        services["asr_service"].pause(False)
        services["sound_detect_service"].subscribe("chatbot")
        # services["asr_service"].subscribe("Test_ASR")
        services["asr_service"].subscribe("activation")
        print("Audio services subscribed")
        return 0
    
    def shutdown(self, services):
        services["asr_service"].pause(True)
        services["asr_service"].removeAllContext()
        services["asr_service"].pause(False)
        services["sound_detect_service"].unsubscribe("chatbot")
        # services["asr_service"].unsubscribe("Test_ASR")
        services["asr_service"].unsubscribe("activation")
        print("Audio services unsubscribed")
        

    # def main(session):
    def run(self, services):
        try:
            buffer = None
            # memory_service.getData("WordRecognized") = [word, confidence]
            # memory_service.getData("SoundDetected") = [index, type, confidence, time]
            
            # Detect and record speech
            # while time.time() - start_time < 20:
            buf = time.time()
            while True:
                try:
                    if time.time() - buf > 1:
                        # print(services["memory_service"].getData("WordRecognized"))
                        buf = time.time()
                    # print(services["memory_service"].getData("SpeechDetected"))
                    
                    if (((services["memory_service"].getData("WordRecognized")[0] == "hello") 
                        or (services["memory_service"].getData("WordRecognized")[0] == "pepper"))
                        and (services["memory_service"].getData("WordRecognized")[1] > 0.3)):
                    #     break
                    # if services["memory_service"].getData("SoundDetected")[0][1] == 1:
                        services["tts_service"].say("I'm listening")
                        break
                except TypeError:
                    # print("NoneType")
                    continue
            services["asr_service"].pause(True)
            services["recorder_service"].startMicrophonesRecording(self.nao_path, self.format, self.rate, [0, 0, 1, 0])
            
            buffer = time.time()
            while True:
                if (services["memory_service"].getData("SoundDetected")[0][1] == 0):
                    if (time.time() - buffer > 3):
                        services["recorder_service"].stopMicrophonesRecording()
                        # subprocess.Popen(["scp", "nao@192.168.0.3:/home/nao/test.wav", "/home/user1/pepper-motion-mimicking/audio/"])
                        subprocess.Popen(["scp", "nao@{}:{}".format(self.nao_ip, self.nao_path), self.audio_path])
                        time.sleep(2)
                        break
                else:
                    buffer = time.time()
                        
        except Exception as e:
            print("speech_detection.py: {}".format(e))
            raise KeyboardInterrupt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number. Default: 9559")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://{}:{}".format(args.ip, args.port))
    except RuntimeError:
        print("Can\'t connect to Naoqi at ip \"{}\" on port {}.\n Please check your script arguments. Run with -h option for help.".format(args.ip, args.port))
        sys.exit(1)
    sd = SpeechDetection(args.ip, args.port)
    
    sound_detect_service = session.service("ALSoundDetection")
    recorder_service = session.service("ALAudioRecorder")
    memory_service = session.service("ALMemory")    
    asr_service = session.service("ALSpeechRecognition")
    tts_service = session.service("ALTextToSpeech")
    
    services = {    
                "tts_service": tts_service,
                "sound_detect_service": sound_detect_service,
                "recorder_service": recorder_service,
                "memory_service": memory_service,
                "asr_service": asr_service
                }
        
    sensitivity = 0.55        
    services["sound_detect_service"].setParameter("Sensitivity", sensitivity)
    services["recorder_service"].stopMicrophonesRecording()
    # services["recorder_service"].subscribe("chatbot")
    services["asr_service"].setLanguage("English")

    vocabulary = ["hello", "pepper"]
    services["asr_service"].pause(True)
    try:
        services["asr_service"].setVocabulary(vocabulary, False)
    except:
        print("Already Set\n")
    services["asr_service"].pause(False)

    # Start the speech recognition engine with user Test_ASR
    services["sound_detect_service"].subscribe("chatbot")
    services["asr_service"].subscribe("activation")
    print('Speech recognition engine started')
    
    while True:
        try:
            sd.run(services)
            test = sd.transcribe_audio(sd.audio_path + "query.wav")
            sd.generate_response(test)
        except KeyboardInterrupt:
            break
    sd.shutdown(services=services)