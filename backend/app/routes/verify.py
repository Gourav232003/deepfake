import cv2
import numpy as np
from flask import Blueprint, current_app, jsonify, request

from app.services.auth_store import get_record
from app.services.crypto import sha256_hex, verify_signature
from app.services.validation import validate_upload
from app.services.watermark import BLOCK_SIZE, extract_content_id
from app.utils.errors import UnprocessableFileError

verify_bp = Blueprint("verify", __name__, url_prefix="/api/verify")

CONTENT_ID_HEX_LENGTH = 32  # uuid4().hex length
CONTENT_ID_BIT_LENGTH = CONTENT_ID_HEX_LENGTH * 4


def _bits_to_content_id(bits: str) -> str:
    hex_chars = []
    for i in range(0, len(bits), 4):
        nibble = bits[i : i + 4]
        hex_chars.append(f"{int(nibble, 2):x}")
    return "".join(hex_chars)


@verify_bp.route("/image", methods=["POST"])
def verify_image():
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
        return jsonify(
            {"success": True, "data": {"status": "no_watermark_found", "reason": "image_too_small_to_carry_watermark"}}
        )

    ycrcb = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2YCrCb)
    y_channel, _, _ = cv2.split(ycrcb)
    recovered_bits = extract_content_id(y_channel, CONTENT_ID_BIT_LENGTH)
    content_id = _bits_to_content_id(recovered_bits)

    record = get_record(content_id)
    if record is None:
        return jsonify({"success": True, "data": {"status": "no_watermark_found", "content_id_attempted": content_id}})

    current_hash = sha256_hex(raw_bytes)
    signature_valid = verify_signature(content_id, record["sha256_hash"], record["signature"], current_app.config["HMAC_SECRET_KEY"])

    if not signature_valid:
        return jsonify({"success": True, "data": {"status": "invalid_signature", "content_id": content_id}})

    if current_hash != record["sha256_hash"]:
        return jsonify(
            {
                "success": True,
                "data": {
                    "status": "tampered_after_signing",
                    "content_id": content_id,
                    "original_hash": record["sha256_hash"],
                    "current_hash": current_hash,
                },
            }
        )

    return jsonify(
        {
            "success": True,
            "data": {"status": "verified_original", "content_id": content_id, "detected_mime": meta["detected_mime"]},
        }
    )
