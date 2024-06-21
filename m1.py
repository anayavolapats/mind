import cv2
import numpy as np

def play_fullscreen_white_noise():
    # Get screen resolution
    screen_width, screen_height = 1440, 900  # Adjust as needed for your screen resolution

    # Create a fullscreen black window
    fullscreen = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

    # Set window size to match screen resolution
    cv2.namedWindow('White Noise', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('White Noise', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        # Generate noise frame
        noise_frame = np.random.randint(0, 256, (screen_height, screen_width, 3), dtype=np.uint8)

        # Show noise frame
        cv2.imshow('White Noise', noise_frame)

        # Exit if '1' key is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('1'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    play_fullscreen_white_noise()
