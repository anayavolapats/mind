import cv2

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

if __name__ == "__main__":
    video_file = '/Users/yanatsapalova/hci_lab/restarted/media/stage6vis.mp4'  # Replace with your video file path

    play_video(video_file)
