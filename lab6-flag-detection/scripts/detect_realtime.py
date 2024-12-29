"""
Script for real-time flag detection using a YOLO model and OpenCV.

This script captures video from the default camera (index 0), attempts
to set a resolution of 1920x1080, and runs inference using a YOLO model
to detect predefined flag classes (Poland, Russia, Ukraine).

Press 'q' to quit the live detection window.
"""

import cv2
from ultralytics import YOLO

def main():
    """
    Runs real-time detection of flags using a YOLO model.

    Steps:
    1. Load a YOLO model for inference (user must specify the path).
    2. Open the default camera (index 0).
    3. Attempt to set the camera resolution to 1920x1080.
    4. In a loop:
       - Read frames from the camera.
       - Run YOLO prediction with a confidence threshold.
       - Draw bounding boxes and labels on detected flags.
       - Display the result in a resizable OpenCV window.
    5. Exit upon pressing 'q'.
    """

    # TODO: Update the path to your actual YOLO file
    model = YOLO("path/to/best.pt")

    # Open default camera
    cap = cv2.VideoCapture(0)

    # Try setting camera resolution to 1920x1080 (may be ignored if unsupported)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Allow the user to resize the window manually
    cv2.namedWindow("Detekcja flag na żywo", cv2.WINDOW_NORMAL)

    # Classes recognized by the model:
    class_names = ["polska", "rosja", "ukraina"]

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Nie można odczytać klatki z kamerki. Zamykanie...")
            break

        # Run YOLO prediction on the current frame
        results = model.predict(frame, conf=0.5)  # conf=0.5 -> detection threshold

        # Iterate over detection results
        for r in results:
            for box in r.boxes:
                # Convert float coordinates to integers
                x1, y1, x2, y2 = box.xyxy[0]
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])

                # Label: class name + confidence score
                label = f"{class_names[cls_id]} {conf:.2f}"

                # Draw bounding box
                cv2.rectangle(
                    frame,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (0, 255, 0),  # box color (green)
                    2             # box thickness
                )

                # Draw text label above the bounding box
                cv2.putText(
                    frame,
                    label,
                    (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),  # text color (green)
                    2             # text thickness
                )

        # Show the frame with detections
        cv2.imshow("Detekcja flag na żywo", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
