import os

from gtts import gTTS
from playsound import playsound

def tts_hello(name):
    # Generate text to be spoken
    text_to_say = f"Hello {name}"

    # Use gTTS to create an mp3 file
    tts = gTTS(text=text_to_say, lang='en')
    tts.save('hello.mp3')

    # Play the generated audio file
    playsound('hello.mp3')

    # Clean up: delete the generated audio file
    os.remove('hello.mp3')

if __name__ == "__main__":
    name = "Patient"  # Replace with the desired name variable

    tts_hello(name)
