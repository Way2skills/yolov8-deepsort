import cv2
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load YOLO models
models = [
    YOLO("FishInv.pt"),
    YOLO("MegaFauna.pt")
]

# Initialize DeepSORT tracker
tracker = DeepSort(max_age=30)  # Keeps track of objects for 30 frames

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    detections = []
    class_labels = {}

    # Perform detection using both models
    for i, model in enumerate(models):
        results = model(frame, conf=[0.522, 0.6][i])  # Apply model-specific confidence threshold

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Convert box coordinates to integers
                conf = box.conf[0].item()  # Confidence score
                cls = int(box.cls[0])  # Class ID
                class_name = model.names[cls]  # Get class name from YOLO model
                
                # Store detection (DeepSORT expects [x, y, width, height, confidence, class])
                detections.append(([x1, y1, x2 - x1, y2 - y1], conf, cls))
                class_labels[cls] = class_name  # Map class ID to name

    # Track objects using DeepSORT
    tracked_objects = tracker.update_tracks(detections, frame=frame)

    # Draw bounding boxes and class names
    for track in tracked_objects:
        if not track.is_confirmed():
            continue

        x1, y1, w, h = map(int, track.to_ltrb())  # Get tracked object's bounding box
        cls_id = track.det_class  # Get class ID
        class_name = class_labels.get(cls_id, "Unknown")  # Get class name

        # Draw bounding box and class name
        cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)
        cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("YOLO + DeepSORT Tracking", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
