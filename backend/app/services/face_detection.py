"""
Face detection with the fallback chain specified in the project brief:
OpenCV DNN detector -> Haar Cascade -> center-crop.

Each detected face reports which method found it, so results stay honest
about detection confidence (a center-crop "face" is a fallback guess, not
a real detection).
"""
from dataclasses import dataclass

import cv2
import numpy as np

DNN_CONFIDENCE_THRESHOLD = 0.6


@dataclass
class DetectedFace:
    x: int
    y: int
    w: int
    h: int
    detector_used: str  # "dnn" | "haar" | "center_crop"


class FaceDetector:
    def __init__(self, dnn_prototxt: str | None = None, dnn_weights: str | None = None):
        self._dnn_net = None
        if dnn_prototxt and dnn_weights:
            self._dnn_net = cv2.dnn.readNetFromCaffe(dnn_prototxt, dnn_weights)

        self._haar = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def detect(self, bgr_image: np.ndarray) -> list[DetectedFace]:
        faces = self._detect_dnn(bgr_image)
        if faces:
            return faces

        faces = self._detect_haar(bgr_image)
        if faces:
            return faces

        return [self._center_crop_fallback(bgr_image)]

    def _detect_dnn(self, bgr_image: np.ndarray) -> list[DetectedFace]:
        if self._dnn_net is None:
            return []
        h, w = bgr_image.shape[:2]
        blob = cv2.dnn.blobFromImage(bgr_image, 1.0, (300, 300), (104.0, 177.0, 123.0))
        self._dnn_net.setInput(blob)
        detections = self._dnn_net.forward()

        faces = []
        for i in range(detections.shape[2]):
            confidence = float(detections[0, 0, i, 2])
            if confidence < DNN_CONFIDENCE_THRESHOLD:
                continue
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            x1, y1, x2, y2 = box.astype(int)
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            if x2 > x1 and y2 > y1:
                faces.append(DetectedFace(x1, y1, x2 - x1, y2 - y1, "dnn"))
        return faces

    def _detect_haar(self, bgr_image: np.ndarray) -> list[DetectedFace]:
        gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        rects = self._haar.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
        return [DetectedFace(int(x), int(y), int(w), int(h), "haar") for (x, y, w, h) in rects]

    def _center_crop_fallback(self, bgr_image: np.ndarray) -> DetectedFace:
        h, w = bgr_image.shape[:2]
        side = min(h, w)
        x = (w - side) // 2
        y = (h - side) // 2
        return DetectedFace(x, y, side, side, "center_crop")


def crop_and_resize_face(bgr_image: np.ndarray, face: DetectedFace, size: int = 224) -> np.ndarray:
    crop = bgr_image[face.y : face.y + face.h, face.x : face.x + face.w]
    return cv2.resize(crop, (size, size), interpolation=cv2.INTER_AREA)
