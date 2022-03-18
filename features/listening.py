import random
import speech_recognition as sr
import features.constant as c
from features.speaker import Speaks as sp

# INITIALIZING THE VOICE RECOGNIZER
record = sr.Recognizer ()


#  DEFINING THE CLASS TO LISTEN THE VOICE AND RECOGNIZE THE ERROR SOUND 
class Listen:


    def record_audio():
        with sr.Microphone() as source:
            audio = record.listen(source)

            try:
                voice_data = record.recognize_google(audio)
                print(f'Yukesh: {voice_data}')
                
            except sr.UnknownValueError:
                sp(random.choice(c.error_msg)).speak()
                return "None"

            except sr.RequestError:
                sp('Sorry,my speech service is down').speak()
            return voice_data
    
