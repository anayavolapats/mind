import cv2
import time
import numpy as np

def perform_blink_tracking():
    # Load the pre-trained model for face and eye detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Open a video stream (adjust camera index or video file path as needed)
    cap = cv2.VideoCapture(1)  # 0 for default camera, or provide a path to a video file

    if not cap.isOpened():
        print("Error: Could not open video stream or file.")
        return

    # Get screen resolution
    screen_width, screen_height = 1920, 1080  # Adjust as per your screen resolution

    # Create a full-screen window
    cv2.namedWindow('Blink Tracking', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Blink Tracking', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Start time for tracking duration
    start_time = time.time()

    # Initialize variables for zooming on eyes
    zoom_factor = 10.5  # Zoom factor for eyes
    blink_detected = False
    blink_counter = 0

    while time.time() - start_time < 10:  # Track blinks for 10 seconds
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale for face and eye detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Loop over detected faces
        for (x, y, w, h) in faces:
            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Extract the region of interest (ROI) for eyes
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            # Detect eyes within the face ROI
            eyes = eye_cascade.detectMultiScale(roi_gray)

            # Loop over detected eyes
            for (ex, ey, ew, eh) in eyes:
                # Draw a rectangle around each eye
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

                # Check for blink (example condition based on eye aspect ratio)
                if blink_detected:
                    # Zoom in on the eyes region
                    roi_startX = max(0, x + ex - int(ew * zoom_factor))
                    roi_startY = max(0, y + ey - int(eh * zoom_factor))
                    roi_endX = min(frame.shape[1], x + ex + ew + int(ew * zoom_factor))
                    roi_endY = min(frame.shape[0], y + ey + eh + int(eh * zoom_factor))

                    # Zoomed eyes ROI
                    eyes_roi = frame[roi_startY:roi_endY, roi_startX:roi_endX]
                    eyes_roi = cv2.resize(eyes_roi, (frame.shape[1], frame.shape[0]))  # Resize back to frame size
                    frame[roi_startY:roi_endY, roi_startX:roi_endX] = eyes_roi

                    # Display "Blink Fast" text
                    cv2.putText(frame, "Blink Fast", (x + ex, y + ey - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Reset blink detection flag
                    blink_detected = False

        # Display the output frame
        cv2.imshow("Blink Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video stream and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    perform_blink_tracking()
