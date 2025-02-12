# from google.cloud import speech
import io
import os
import time
import sys
import re
import socket
import subprocess
import select
import glob
import argparse
import threading
# from pydub import AudioSegment
# from gptpy3.chat_client import ChatClient
from assistant import ChatGPT, LlamaAssistant
import whisper


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = glob.glob(os.path.expanduser("~") + "/current_key/*.json")[0]

class WhisperSTT():
    def __init__(self, model_size: str="small") -> None:
        self.model = whisper.load_model(model_size)
    
    def get_transcribe(self, audio: str, language: str = "en"):
        result = self.model.transcribe(audio=audio, language=language, verbose=False)
        return result.get('text', '')


client = None

def connect(ip, port):
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("{}, {}".format(ip, port))
    client.connect((ip, port))
    print(f"Connected to {port}.")
    
def disconnect():
    global client
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    
def test():
    llama = LlamaAssistant(system_prompt=None)
    whisper = WhisperSTT()
    
    response = whisper.get_transcribe("/home/user1/pepper-motion-mimicking/audio/query.wav")
    received_msg = llama.chat(response)
    print(received_msg)
                
    
    
def main():
    global client
    llama = LlamaAssistant(system_prompt=None)
    whisper = WhisperSTT()
    try:
        while True:
            if client is None:
                print("GPT client not connected")
                time.sleep(1)
                continue
            audio_file = client.recv(1024)
            
            # if not buf:
            if not audio_file:
                break
            time.sleep(1)
            response = whisper.get_transcribe(audio_file.decode())
            print(response)
            
            # response = GoogleSTT.transcribe_file(audio_file)  
            if response == "q":
                client.sendall("011".encode())
                break
            if response == "":
                client.sendall("010".encode())
            else:
                # received_msg = gpt.chat_test(response)
                received_msg = llama.chat(response)
                print(received_msg)
                client.sendall(received_msg.encode())
                
    except KeyboardInterrupt:
        print("\nException")
    

    # gpt.delete_assistant(names="Pepper")
    print("Closed GPT")    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=3434,
                        help="Naoqi port number")
    
    args = parser.parse_args()
    
    _client = threading.Thread(target=connect, name='connect', args = (args.ip, args.port))
    _client.start()
    
    # gpt = ChatGPT(secret_key_path="/home/user1/secret-key.txt")
    # gpt.create_assistant(name="Pepper")
    
    main()
    # test()
    _client.join()
    disconnect()
    print("Closed Client")
    
    

                         

# class GoogleSTT():
#     def transcribe_file(audio_file: str) -> speech.RecognizeResponse:
#         """Transcribe the given audio file.
#         Args:
#             audio_file (str): Path to the local audio file to be transcribed.
#                 Example: "resources/audio.wav"
#         Returns:
#             cloud_speech.RecognizeResponse: The response containing the transcription results
#         """
#         ret = "Repeat the following: I didn't hear that, please try again"  # Default response if no speech is detected
        
#         client = speech.SpeechClient()

#         with open(audio_file, "rb") as f:
#             audio_content = f.read()

#         audio = speech.RecognitionAudio(content=audio_content)
#         config = speech.RecognitionConfig(
#             encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#             sample_rate_hertz=44100,
#             language_code="en-US",
#         )

#         response = client.recognize(config=config, audio=audio)

#         # Each result is for a consecutive portion of the audio. Iterate through
#         # them to get the transcripts for the entire audio file.
#         for result in response.results:
#             # The first alternative is the most likely one for this portion.
#             # print(f"Transcript: {result.alternatives[0].transcript}")
#             ret = result.alternatives[0].transcript

#         # return response
#         return ret

#     def run_quickstart(audio) -> speech.RecognizeResponse:
#         # Instantiates a client
#         client = speech.SpeechClient()
#         audio_list = [audio]
        
#         requests = (
#             speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_list
#         )

#         config = speech.RecognitionConfig(
#             encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#             sample_rate_hertz=44100,
#             language_code="en-US",
#         )

#         streaming_config = speech.StreamingRecognitionConfig(config=config)

#         # streaming_recognize returns a generator.
#         responses = client.streaming_recognize(
#             config=streaming_config,
#             requests=requests,
#         )
#         sttresult = "Repeat this phrase: I'm sorry, I didn't quite hear that" # Default phrase if STT cannot detect speech
#         for response in responses:
#             for result in response.results:
#                 alternatives = result.alternatives
#                 for alternative in alternatives:
#                     sttresult = alternative.transcript
                    
#         return sttresult    