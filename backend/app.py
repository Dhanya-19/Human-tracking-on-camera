from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

import cv2
import numpy as np
import time

from detector.inference import process_frame

import shared_frame
import threat_state


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload_frame")
async def upload_frame(file: UploadFile = File(...)):

    contents = await file.read()

    npimg = np.frombuffer(
        contents,
        np.uint8
    )

    frame = cv2.imdecode(
        npimg,
        cv2.IMREAD_COLOR
    )

    if frame is not None:

        shared_frame.latest_frame = frame

    return {"status": "ok"}


def generate_frames():

    while True:

        try:

            if shared_frame.latest_frame is None:

                time.sleep(0.03)
                continue

            frame = shared_frame.latest_frame.copy()

            annotated_frame, persons, alert = (
                process_frame(frame)
            )

            if annotated_frame is None:

                continue

            success, buffer = cv2.imencode(
                '.jpg',
                annotated_frame,
                [cv2.IMWRITE_JPEG_QUALITY, 80]
            )

            if not success:

                continue

            frame_bytes = buffer.tobytes()

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n'
                + frame_bytes +
                b'\r\n'
            )

            time.sleep(0.03)

        except Exception as e:

            print("VIDEO STREAM ERROR:", e)

            continue


@app.get("/video_feed")
def video_feed():

    return StreamingResponse(
        generate_frames(),
        media_type='multipart/x-mixed-replace; boundary=frame'
    )


@app.get("/threats")
def get_threats():

    return threat_state.live_threats