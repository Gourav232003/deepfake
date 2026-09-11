import uuid
from datetime import datetime, timezone

import torch
import numpy as np
import cv2
from flask import Blueprint, current_app, jsonify, request

from app.services.face_detection import FaceDetector, crop_and_resize_face
from app.services.inference import DeepfakeImageClassifier, aggregate_video_probability
from app.services.validation import validate_upload
from app.utils.errors import UnprocessableFileError

detect_bp = Blueprint("detect", __name__, url_prefix="/api/detect")

LIMITATIONS_NOTICE = (
    "This result reflects a machine-learning prediction, not forensic "
    "certainty. Accuracy depends on training data and model generalization."
)

# Lazily constructed on first use — avoids loading model weights at import
# time (useful for tests and for routes that don't need them).
_face_detector = None
_image_classifier = None


def _get_face_detector() -> FaceDetector:
    global _face_detector
    if _face_detector is None:
        _face_detector = FaceDetector()  # DNN prototxt/weights wired once available
    return _face_detector


def _get_image_classifier() -> DeepfakeImageClassifier:
    global _image_classifier
    if _image_classifier is None:
        _image_classifier = DeepfakeImageClassifier(checkpoint_path=None)  # placeholder — see inference.py
    return _image_classifier


def _bgr_to_face_tensor(face_bgr: np.ndarray) -> torch.Tensor:
    rgb = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    tensor = torch.from_numpy(rgb).permute(2, 0, 1).unsqueeze(0)
    return tensor


@detect_bp.route("/image", methods=["POST"])
def detect_image():
    file_storage = request.files.get("file")
    meta = validate_upload(
        file_storage,
        allowed_mime=current_app.config["ALLOWED_IMAGE_MIME"],
        max_size_bytes=current_app.config["MAX_IMAGE_SIZE"],
    )

    raw_bytes = file_storage.read()
    np_arr = np.frombuffer(raw_bytes, dtype=np.uint8)
    bgr_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if bgr_image is None:
        raise UnprocessableFileError("File passed validation but could not be decoded as an image.")

    faces = _get_face_detector().detect(bgr_image)
    classifier = _get_image_classifier()

    face_results = []
    probabilities = []
    for i, face in enumerate(faces):
        face_crop = crop_and_resize_face(bgr_image, face, size=224)
        tensor = _bgr_to_face_tensor(face_crop)
        prediction = classifier.predict(tensor)
        probabilities.append(prediction.probability_fake)
        face_results.append(
            {
                "face_id": f"face_{i}",
                "bounding_box": {"x": face.x, "y": face.y, "w": face.w, "h": face.h},
                "probability": prediction.probability_fake,
                "detector_used": face.detector_used,
            }
        )

    overall_probability = max(probabilities) if probabilities else None
    verdict = "no_face_detected" if not probabilities else ("fake" if overall_probability >= 0.5 else "real")

    return jsonify(
        {
            "success": True,
            "data": {
                "result_id": uuid.uuid4().hex,
                "media_type": "image",
                "verdict": verdict,
                "probability": overall_probability,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "evidence": {"faces": face_results, "detected_mime": meta["detected_mime"]},
                "model_notice": classifier.predict.__doc__ or "",
                "limitations_notice": LIMITATIONS_NOTICE,
            },
        }
    )


@detect_bp.route("/video", methods=["POST"])
def detect_video():
    """
    Scaffold: validates the upload and defines the response shape. Frame
    extraction + per-frame classification + the fixed aggregation formula
    (see services/inference.py::aggregate_video_probability) are Phase 6
    work per ImplementationPlan.md — not yet wired here.
    """
    file_storage = request.files.get("file")
    meta = validate_upload(
        file_storage,
        allowed_mime=current_app.config["ALLOWED_VIDEO_MIME"],
        max_size_bytes=current_app.config["MAX_VIDEO_SIZE"],
    )

    # TODO (Phase 6): extract frames at current_app.config["FRAME_SAMPLE_RATE_HZ"],
    # run each through the same face-detect + classify pipeline as
    # detect_image, collect frame_probabilities, then:
    #   overall_probability = aggregate_video_probability(frame_probabilities)
    raise UnprocessableFileError(
        "Video detection pipeline is not yet implemented (Phase 6). "
        f"Upload validated successfully as {meta['detected_mime']}."
    )


@detect_bp.route("/audio", methods=["POST"])
def detect_audio():
    """
    Scaffold: validates the upload and defines the response shape. The
    16kHz resample -> log-Mel -> CNN+BiLSTM pipeline is Phase 7 work per
    ImplementationPlan.md — not yet wired here.
    """
    file_storage = request.files.get("file")
    meta = validate_upload(
        file_storage,
        allowed_mime=current_app.config["ALLOWED_AUDIO_MIME"],
        max_size_bytes=current_app.config["MAX_AUDIO_SIZE"],
    )

    # TODO (Phase 7): librosa.load(..., sr=current_app.config["AUDIO_TARGET_SAMPLE_RATE"]),
    # compute log-Mel with current_app.config["AUDIO_MEL_BANDS"] bands, run
    # through the CNN+BiLSTM model.
    raise UnprocessableFileError(
        "Audio detection pipeline is not yet implemented (Phase 7). "
        f"Upload validated successfully as {meta['detected_mime']}."
    )
