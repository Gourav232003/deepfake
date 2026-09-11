import uuid
from datetime import datetime, timezone

import cv2
import numpy as np
from flask import Blueprint, current_app, jsonify, request

from app.services.auth_store import save_record
from app.services.crypto import generate_content_id, sha256_hex, sign_content
from app.services.validation import validate_upload
from app.services.watermark import BLOCK_SIZE, embed_content_id
from app.utils.errors import UnprocessableFileError

authenticate_bp = Blueprint("authenticate", __name__, url_prefix="/api/authenticate")


def _content_id_to_bits(content_id_hex: str) -> str:
    return "".join(f"{int(c, 16):04b}" for c in content_id_hex)


@authenticate_bp.route("/image", methods=["POST"])
def authenticate_image():
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

    h, w = bgr_image.shape[:2]
    if h < BLOCK_SIZE * 8 or w < BLOCK_SIZE * 8:
        raise UnprocessableFileError(
            f"Image is too small to embed a reliable watermark (minimum ~{BLOCK_SIZE * 8}px per side)."
        )

    content_id = generate_content_id()

    ycrcb = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2YCrCb)
    y_channel, cr, cb = cv2.split(ycrcb)
    watermarked_y = embed_content_id(y_channel, _content_id_to_bits(content_id))
    watermarked_image = cv2.cvtColor(cv2.merge([watermarked_y, cr, cb]), cv2.COLOR_YCrCb2BGR)

    success, encoded = cv2.imencode(".png", watermarked_image)
    if not success:
        raise UnprocessableFileError("Failed to encode the watermarked image for output.")

    # IMPORTANT: hash the watermarked bytes (what the user actually walks away
    # with and will re-upload for verification), not the pre-watermark
    # original. Hashing the original here would make every honest
    # verification of the (necessarily different) watermarked file report
    # as "tampered", which is wrong.
    watermarked_bytes = encoded.tobytes()
    original_hash = sha256_hex(watermarked_bytes)

    signature = sign_content(content_id, original_hash, current_app.config["HMAC_SECRET_KEY"])
    save_record(content_id, original_hash, signature)
    # `signature` is persisted server-side only (see Schema.md's open
    # persistence question) — it is deliberately NOT included below.

    return jsonify(
        {
            "success": True,
            "data": {
                "content_id": content_id,
                "sha256_hash": original_hash,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "watermarked_image_base64": watermarked_bytes.hex(),  # scaffold transport; swap for a file URL in Phase 9
                "detected_mime": meta["detected_mime"],
            },
        }
    )
