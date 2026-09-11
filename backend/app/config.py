import os


class Config:
    """
    Central configuration. Values come from environment variables so that
    secrets (HMAC_SECRET_KEY especially) never live in source control.
    """

    # --- Core ---
    ENV = os.environ.get("FLASK_ENV", "development")
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH_BYTES", 100 * 1024 * 1024))  # 100 MB hard cap

    # --- Per-media upload limits (bytes) ---
    MAX_IMAGE_SIZE = int(os.environ.get("MAX_IMAGE_SIZE_BYTES", 15 * 1024 * 1024))   # 15 MB
    MAX_VIDEO_SIZE = int(os.environ.get("MAX_VIDEO_SIZE_BYTES", 100 * 1024 * 1024))  # 100 MB
    MAX_AUDIO_SIZE = int(os.environ.get("MAX_AUDIO_SIZE_BYTES", 25 * 1024 * 1024))   # 25 MB

    # --- Allowed types ---
    ALLOWED_IMAGE_MIME = {"image/jpeg", "image/png", "image/webp"}
    ALLOWED_VIDEO_MIME = {"video/mp4", "video/quicktime", "video/x-matroska"}
    ALLOWED_AUDIO_MIME = {"audio/wav", "audio/x-wav", "audio/mpeg", "audio/flac"}

    # --- Video processing ---
    MAX_VIDEO_DURATION_SEC = int(os.environ.get("MAX_VIDEO_DURATION_SEC", 120))
    FRAME_SAMPLE_RATE_HZ = float(os.environ.get("FRAME_SAMPLE_RATE_HZ", 1.0))  # frames sampled per second

    # --- Audio processing ---
    AUDIO_TARGET_SAMPLE_RATE = 16000
    AUDIO_MEL_BANDS = 128

    # --- Authentication / crypto ---
    # NEVER commit a real value here. Must be set via environment in every
    # deployment. Never returned in any API response.
    HMAC_SECRET_KEY = os.environ.get("DEEPGUARD_HMAC_SECRET_KEY")

    # --- Storage ---
    UPLOAD_TMP_DIR = os.environ.get("UPLOAD_TMP_DIR", "/tmp/deepguard_uploads")

    @classmethod
    def validate(cls):
        """Fail loudly at startup rather than silently at request time."""
        if cls.ENV != "development" and not cls.HMAC_SECRET_KEY:
            raise RuntimeError(
                "DEEPGUARD_HMAC_SECRET_KEY must be set outside development. "
                "Refusing to start with no signing secret configured."
            )
