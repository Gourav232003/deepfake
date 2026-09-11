"""
Minimal persistence for authentication records, keyed by content_id.

STATUS: PLACEHOLDER. Schema.md flags this as an open question — whether
verification should be fully self-contained in the watermark+signature (no
store at all) or backed by a lookup. This JSON-file store is the smallest
thing that lets the four verification states (Verified / Tampered /
Invalid-Forged / No Watermark) actually be implemented end-to-end for the
scaffold; swap for SQLite/a real DB or remove entirely once that question
is resolved, per ImplementationPlan.md item 3.

Never stores the HMAC secret itself — only per-content signatures, which
are meaningless without the server's secret key.
"""
import json
import os
import threading

_LOCK = threading.Lock()
_STORE_PATH = os.environ.get("DEEPGUARD_AUTH_STORE_PATH", "/tmp/deepguard_auth_store.json")


def _read_all() -> dict:
    if not os.path.exists(_STORE_PATH):
        return {}
    with open(_STORE_PATH, "r") as f:
        return json.load(f)


def _write_all(data: dict) -> None:
    with open(_STORE_PATH, "w") as f:
        json.dump(data, f)


def save_record(content_id: str, sha256_hash: str, signature: str) -> None:
    with _LOCK:
        data = _read_all()
        data[content_id] = {"sha256_hash": sha256_hash, "signature": signature}
        _write_all(data)


def get_record(content_id: str) -> dict | None:
    with _LOCK:
        return _read_all().get(content_id)
