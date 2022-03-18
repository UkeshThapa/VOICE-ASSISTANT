import pyttsx3


class Speaks:
    def __init__(self,data):
        self.data= data

    def speak(self):
        engine = pyttsx3.init('sapi5')
        voices= engine.getProperty('voices') #getting details of current voice
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 178)
        print(f'Penny: {self.data}')
        engine.say(self.data) 
        engine.runAndWait() #Without this command, speech will not be audible to us.
