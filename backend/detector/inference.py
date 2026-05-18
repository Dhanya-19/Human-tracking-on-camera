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

            score, level, color, activity = (
                calculate_threat_score(track_id)
            )

            threat_state.live_threats.append({

                "id": int(track_id),

                "score": int(score),

                "level": level,

                "activity": activity,

                "event": f"{activity} DETECTED"

            })

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