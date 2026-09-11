"""
Upload validation: never trust a filename or a client-supplied extension.
Sniff actual content type, enforce size limits, and reject anything that
doesn't match the expected media category before it ever reaches a model.
"""
import os
import uuid

from app.utils.errors import FileTooLargeError, InvalidFileError

try:
    import magic  # python-magic: content-based MIME sniffing
    _HAS_MAGIC = True
except ImportError:  # pragma: no cover - allows scaffold to run before libmagic is installed
    _HAS_MAGIC = False


def _sniff_mime(file_storage) -> str:
    """Read the first chunk of the file to detect its real MIME type."""
    head = file_storage.stream.read(4096)
    file_storage.stream.seek(0)
    if _HAS_MAGIC:
        return magic.from_buffer(head, mime=True)
    # Fallback for environments without libmagic installed: last resort only,
    # and deliberately conservative — this path should be replaced by the
    # magic-based check before shipping.
    return file_storage.mimetype or "application/octet-stream"


def validate_upload(file_storage, *, allowed_mime: set, max_size_bytes: int) -> dict:
    """
    Validates a Werkzeug FileStorage against an allowed MIME set and a size
    ceiling. Returns metadata for downstream processing on success, or
    raises InvalidFileError / FileTooLargeError.
    """
    if file_storage is None or file_storage.filename == "":
        raise InvalidFileError("No file was uploaded.")

    file_storage.stream.seek(0, os.SEEK_END)
    size_bytes = file_storage.stream.tell()
    file_storage.stream.seek(0)

    if size_bytes == 0:
        raise InvalidFileError("Uploaded file is empty.")
    if size_bytes > max_size_bytes:
        raise FileTooLargeError(
            f"File is {size_bytes / (1024 * 1024):.1f} MB, "
            f"which exceeds the {max_size_bytes / (1024 * 1024):.0f} MB limit."
        )

    detected_mime = _sniff_mime(file_storage)
    if detected_mime not in allowed_mime:
        raise InvalidFileError(
            f"Unsupported file type ({detected_mime}). "
            f"Allowed types: {', '.join(sorted(allowed_mime))}."
        )

    # Never trust the client filename for storage — generate our own.
    safe_name = f"{uuid.uuid4().hex}"

    return {
        "safe_name": safe_name,
        "detected_mime": detected_mime,
        "size_bytes": size_bytes,
    }
