"""
Hashing and signing for image authentication. HMAC_SECRET_KEY is read from
Config (environment) and is NEVER returned in any response body — see
Rules.md's "Never expose HMAC keys" rule and TechSpec.md's Security section.
"""
import hashlib
import hmac
import uuid


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def generate_content_id() -> str:
    return uuid.uuid4().hex


def sign_content(content_id: str, sha256_hash: str, secret_key: str) -> str:
    """Returns a hex HMAC-SHA256 signature over `content_id + sha256_hash`."""
    if not secret_key:
        raise RuntimeError("HMAC secret key is not configured.")
    message = f"{content_id}:{sha256_hash}".encode("utf-8")
    return hmac.new(secret_key.encode("utf-8"), message, hashlib.sha256).hexdigest()


def verify_signature(content_id: str, sha256_hash: str, signature: str, secret_key: str) -> bool:
    expected = sign_content(content_id, sha256_hash, secret_key)
    # Constant-time comparison to avoid timing side-channels.
    return hmac.compare_digest(expected, signature)
