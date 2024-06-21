import cv2
from deepface import DeepFace
from gtts import gTTS
import os
import pygame
import time

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("emotion.mp3")
    pygame.mixer.music.load("emotion.mp3")
    pygame.mixer.music.play()

def main():
    # Initialize Pygame for audio playback
    pygame.init()
    pygame.mixer.init()

    # Print the path to cascade XML file for debugging
    print(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Load face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Start capturing video from webcam (change the index as needed)
    cap_webcam = cv2.VideoCapture(0)

    # Open a pre-saved video file (replace with your video file path)
    video_file_path = "/Users/yanatsapalova/hci_lab/restarted/media/emotions.mp4"
    cap_video = cv2.VideoCapture(video_file_path)

    # Check if both captures are opened successfully
    if not cap_webcam.isOpened() or not cap_video.isOpened():
        print("Error: One or more video streams could not be opened.")
        return

    speak_counter = 0  # Counter to limit TTS frequency
    swap_counter = 0  # Counter to control screen swapping

    while True:
        # Capture frame from webcam
        ret_webcam, frame_webcam = cap_webcam.read()

        # Capture frame from pre-saved video
        ret_video, frame_video = cap_video.read()

        if not ret_webcam or not ret_video:
            break

        # Convert frames to grayscale for emotion detection
        gray_frame_webcam = cv2.cvtColor(frame_webcam, cv2.COLOR_BGR2GRAY)
        rgb_frame_webcam = cv2.cvtColor(gray_frame_webcam, cv2.COLOR_GRAY2RGB)

        # Detect faces in the webcam frame
        faces_webcam = face_cascade.detectMultiScale(gray_frame_webcam, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces_webcam:
            face_roi_webcam = rgb_frame_webcam[y:y + h, x:x + w]
            result_webcam = DeepFace.analyze(face_roi_webcam, actions=['emotion'], enforce_detection=False)
            emotion_webcam = result_webcam[0]['dominant_emotion']

            # Draw rectangle around face and label with predicted emotion
            cv2.rectangle(frame_webcam, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame_webcam, emotion_webcam, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            # Speak the detected emotion less frequently
            if speak_counter % 50 == 0:  # Adjust this value to control frequency
                speak(emotion_webcam)

        speak_counter += 1

        # Resize the pre-saved video frame to be smaller
        height, width, _ = frame_webcam.shape
        small_frame_video = cv2.resize(frame_video, (width // 3, height // 3))

        # Swap the screens every few frames
        if swap_counter % 100 == 0:  # Adjust this value to control swap frequency
            main_frame, overlay_frame = frame_webcam, small_frame_video
        else:
            main_frame, overlay_frame = frame_video, cv2.resize(frame_webcam, (width // 3, height // 3))

        swap_counter += 1

        # Overlay the small video frame on the bottom-right corner of the main frame
        main_frame[-overlay_frame.shape[0]:, -overlay_frame.shape[1]:] = overlay_frame

        # Display the combined frame in fullscreen
        cv2.namedWindow('Combined', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Combined', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Combined', main_frame)

        # Check for exit key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture objects and close all windows
    cap_webcam.release()
    cap_video.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()

if __name__ == "__main__":
    main()
