from ultralytics import YOLO
import cv2
from detector.threat_analysis import (
    calculate_threat_score,
    cleanup_old_tracks,
    RESTRICTED_ZONE  # Imported to draw it visually on the screen
)
import threat_state

model = YOLO("yolov8n.pt")

def process_frame(frame):
    cleanup_old_tracks()

    # --- SMART INITIAL SAFEGUARD ---
    # Check if the incoming frame data is completely empty or pitch black
    # This prevents the red ROI box from showing up before the stream officially begins!
    if frame is None or cv2.countNonZero(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)) == 0:
        return frame, 0, None

    results = model.track(
        source=frame,
        persist=True,
        verbose=False,
        tracker="bytetrack.yaml",
        conf=0.45,
        iou=0.5,
        classes=[0]
    )

    annotated_frame = frame.copy()
    
    # --- VISUAL FEATURE FOR EVALUATORS: Draw the Restricted Zone ---
    # RESTRICTED_ZONE is [x_min, y_min, x_max, y_max]
    rx1, ry1, rx2, ry2 = RESTRICTED_ZONE
    
    # Create a semi-transparent overlay for the restricted zone
    overlay = annotated_frame.copy()
    cv2.rectangle(overlay, (rx1, ry1), (rx2, ry2), (0, 0, 255), -1)  # Solid Red fill
    # Blend the overlay with the original frame (alpha transparency = 0.25)
    cv2.addWeighted(overlay, 0.25, annotated_frame, 0.75, 0, annotated_frame)
    
    # Add a border and label to the Restricted Zone
    cv2.rectangle(annotated_frame, (rx1, ry1), (rx2, ry2), (0, 0, 255), 2)
    cv2.putText(
        annotated_frame, 
        "CRITICAL SECURITY ZONE", 
        (rx1 + 10, ry1 + 30), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        0.7, 
        (0, 0, 255), 
        2
    )
    # ---------------------------------------------------------------

    threat_state.live_threats.clear()

    if (
        results
        and results[0].boxes is not None
        and results[0].boxes.id is not None
    ):
        boxes = results[0].boxes.xyxy.cpu().numpy()
        ids = results[0].boxes.id.cpu().numpy()

        for box, track_id in zip(boxes, ids):
            x1, y1, x2, y2 = map(int, box)

            # Safeguard conversion to standard primitive values
            bbox_list = [float(x1), float(y1), float(x2), float(y2)]

            score, level, color, activity = (
                calculate_threat_score(track_id, bbox_list)
            )

            threat_state.live_threats.append({
                "id": int(track_id),
                "score": int(score),
                "level": level,
                "activity": activity,
                "event": f"{activity} DETECTED"
            })

            # Draw the tracking bounding box around the person
            cv2.rectangle(
                annotated_frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            label = (
                f"ID {int(track_id)} "
                f"| {score}% {level} "
                f"| {activity}"
            )

            cv2.putText(
                annotated_frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

    persons = len(threat_state.live_threats)
    alert = None

    if persons >= 5:
        alert = "Crowd Detected"

    return annotated_frame, persons, alert