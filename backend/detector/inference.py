from ultralytics import YOLO
import cv2
from detector.threat_analysis import (
    calculate_threat_score,
    cleanup_old_tracks
)
import threat_state

model = YOLO("yolov8n.pt")

def process_frame(frame):
    cleanup_old_tracks()

    # --- YOUR CRITICAL CHRONOLOGICAL SAFEGUARD CHECK ---
    # We check if the frame is empty or completely black FIRST.
    if frame is None or cv2.countNonZero(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)) == 0:
        return frame, 0, None

    # --- FEEDBACK LOOP SAFEGUARD ---
    # Find the middle point of the incoming frame canvas
    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2

    # Check a shifted 100x100 patch on the left side of the screen.
    # This prevents the drawn red box from getting captured by the check on the next loop!
    status_patch = frame[max(0, cy-50):min(h, cy+50), max(0, cx-200):min(w, cx-100)]
    
    # If the background window patch is black, the screen share is idle. Clear it out.
    if cv2.countNonZero(cv2.cvtColor(status_patch, cv2.COLOR_BGR2GRAY)) == 0:
        return frame, 0, None

    # --- FIXED BOX COORDINATES (STAYS INSIDE THE VIDEO CONTENT) ---
    frame_height, frame_width = frame.shape[:2]

    # Constrained to sit safely inside the active video, avoiding the black sidebars
    rx1 = int(frame_width * 0.48)   # Starts just left of the center line
    rx2 = int(frame_width * 0.72)   # Ends safely before the right black pillarbox padding
    
    ry1 = int(frame_height * 0.35)  # Balanced vertical placement
    ry2 = int(frame_height * 0.78)  
    
    # Update tracking engine boundaries dynamically
    from detector import threat_analysis
    threat_analysis.RESTRICTED_ZONE = [rx1, ry1, rx2, ry2]
    # ---------------------------------------------------------------

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
    
    # Render translucent red zone backdrop profile
    overlay = annotated_frame.copy()
    cv2.rectangle(overlay, (rx1, ry1), (rx2, ry2), (0, 0, 255), -1) 
    cv2.addWeighted(overlay, 0.25, annotated_frame, 0.75, 0, annotated_frame)
    
    # Draw containment border outlines and text banner
    cv2.rectangle(annotated_frame, (rx1, ry1), (rx2, ry2), (0, 0, 255), 2)
    cv2.putText(
        annotated_frame, 
        "CRITICAL SECURITY ZONE", 
        (rx1 + 10, ry1 + 30), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        0.5,  
        (0, 0, 255), 
        2
    )

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

            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)

            label = f"ID {int(track_id)} | {score}% {level} | {activity}"
            cv2.putText(
                annotated_frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )

    persons = len(threat_state.live_threats)
    alert = "Crowd Detected" if persons >= 5 else None

    return annotated_frame, persons, alert