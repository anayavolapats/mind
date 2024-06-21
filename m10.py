import cv2
import mediapipe as mp
import numpy as np
import time
import pygame

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

# Initialize drawing utility
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# Open video capture
cap = cv2.VideoCapture(0)

# Get screen resolution (adjust as needed)
screen_width, screen_height = 1440, 900

# Create a fullscreen window
cv2.namedWindow('Fullscreen Output', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Fullscreen Output', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Initialize variables for blinking effect
blink_speed = 1.0  # Initial delay in seconds
max_blink_speed = 0.1  # Maximum speed to reach in seconds
blink_acceleration = 0.01  # Rate of acceleration

# Time tracking variables
start_time = time.time()

# Initialize pygame for audio playback
pygame.mixer.init()
pygame.mixer.music.load('/Users/yanatsapalova/hci_lab/restarted/media/ethan_evil.mp3')  # Replace with your audio file path
pygame.mixer.music.play()  # Play the audio file once

# Variables for animation
color_index = 0
color_change_speed = 0.05
opacity = 0
opacity_direction = 1

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and find face landmarks
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Create a mask
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            points = np.array([[int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])] for lm in face_landmarks.landmark])
            cv2.fillPoly(mask, [points], 255)

            # Apply the mask to the frame
            masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

            # Create an overlay for animation
            overlay = np.zeros_like(frame, dtype=np.uint8)
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
            current_color = colors[color_index]

            # Update opacity
            opacity += opacity_direction * color_change_speed
            if opacity >= 1.0:
                opacity = 1.0
                opacity_direction = -1
            elif opacity <= 0.0:
                opacity = 0.0
                opacity_direction = 1
                color_index = (color_index + 1) % len(colors)

            # Apply the overlay with transparency
            overlay[mask == 255] = current_color
            cv2.addWeighted(overlay, opacity, masked_frame, 1 - opacity, 0, masked_frame)

            # Display the masked area in fullscreen
            cv2.imshow('Fullscreen Output', masked_frame)

            # Calculate time elapsed
            elapsed_time = time.time() - start_time

            # Blinking effect: switch between normal frame and masked_frame
            if elapsed_time > blink_speed:
                # Update start time for next blink interval
                start_time = time.time()

                # Alternate between showing normal frame and masked_frame
                if blink_speed > max_blink_speed:
                    blink_speed -= blink_acceleration  # Increase blinking speed gradually

    # Check if audio is still playing
    if not pygame.mixer.music.get_busy():
        break

    # Check for 'q' key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop and release audio playback
pygame.mixer.music.stop()

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()
