import cv2
import time
import numpy as np

def perform_object_recognition():
    # Load the pre-trained model for object detection
    net = cv2.dnn.readNetFromCaffe('models/MobileNetSSD_deploy.prototxt.txt', 'models/MobileNetSSD_deploy.caffemodel')

    # Open a video stream (adjust camera index or video file path as needed)
    cap = cv2.VideoCapture(1)  # 0 for default camera, or provide a path to a video file

    if not cap.isOpened():
        print("Error: Could not open video stream or file.")
        return

    # Get screen resolution
    screen_width, screen_height = 1920, 1080  # Adjust as per your screen resolution

    # Create a full-screen window
    cv2.namedWindow('Object Detection', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Object Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Start time for object recognition duration
    start_time = time.time()

    while time.time() - start_time < 10:  # Perform object recognition for 10 seconds
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame for faster processing
        frame_resized = cv2.resize(frame, (300, 300))

        # Prepare input image to run through the network
        blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), 127.5)

        # Set the input to the network and perform inference
        net.setInput(blob)
        detections = net.forward()

        # Loop over the detections
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:  # Filter detections by confidence threshold
                class_id = int(detections[0, 0, i, 1])
                class_name = classNames[class_id]
                print(f"Detected object: {class_name}, Confidence: {confidence:.2f}")

                # Draw bounding box around the detected object
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, class_name, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the output frame
        cv2.imshow("Object Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video stream and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Define the classes (adjust as per your model)
    classNames = {0: 'background', 1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
                  5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair', 10: 'cow',
                  11: 'diningtable', 12: 'dog', 13: 'horse', 14: 'motorbike',
                  15: 'person', 16: 'pottedplant', 17: 'sheep', 18: 'sofa',
                  19: 'train', 20: 'tvmonitor'}

    perform_object_recognition()
