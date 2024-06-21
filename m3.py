import cv2
import os
from gtts import gTTS
from playsound import playsound
import threading

def play_video(video_file):
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get screen resolution (adjust as needed)
    screen_width = 1440  # Replace with your screen width resolution
    screen_height = 900  # Replace with your screen height resolution

    # Set video window size to match screen resolution
    cv2.namedWindow('Video Player', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Video Player', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame to match screen resolution
        frame = cv2.resize(frame, (screen_width, screen_height))

        cv2.imshow('Video Player', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

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
    video_file = '/Users/yanatsapalova/hci_lab/restarted/media/connection.mp4'  # Replace with your video file path
    name = "julia"  # Replace with the desired name variable

    # Start the TTS audio playback in a separate thread
    audio_thread = threading.Thread(target=tts_hello, args=(name,))
    audio_thread.start()

    # Play the video
    play_video(video_file)

    # Wait for the audio thread to finish
    audio_thread.join()
