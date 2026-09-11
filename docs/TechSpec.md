# TechSpec — DeepGuard

## Architecture
```
React + Vite Frontend
        │  REST (JSON, multipart for uploads)
        ▼
Flask Backend (blueprints per domain)
        │
        ├── Image pipeline  (OpenCV DNN face detect → align/crop → EfficientNet-B0 → Grad-CAM)
        ├── Video pipeline  (frame extraction → image pipeline per frame → weighted aggregation)
        ├── Audio pipeline  (resample → log-Mel → CNN+BiLSTM)
        └── Authentication  (SHA-256 + DCT watermark → HMAC-SHA256 sign/verify)
```
No microservices, no queues, no Kubernetes, no distributed DB — single Flask app, single frontend build, per Rules.md.

## Frontend
- Framework: React
- Build Tool: Vite
- Language: JavaScript
- Styling: Tailwind CSS
- Structure: feature-based folders (`upload/`, `results/`, `authenticate/`, `verify/`), shared `api/` client, shared `components/` (buttons, state badges, evidence panels).

## Backend
- Framework: Flask
- API style: REST, JSON responses (multipart/form-data for file upload endpoints)
- Language: Python 3.9+
- Layout: `routes/`, `services/` (inference, video, audio, watermark, crypto), `validation/`, `utils/` — never one monolithic `app.py`.

## AI / ML
- PyTorch, torchvision
- EfficientNet-B0 (image/video face classifier, 224×224 input)
- Custom CNN + 2-layer BiLSTM (audio)
- Grad-CAM (image/video explainability)
- scikit-learn (evaluation metrics)

## Computer Vision
- OpenCV DNN face detector (primary)
- Haar Cascade (fallback)
- Center-crop (final fallback when no face detector succeeds)

## Audio
- librosa, soundfile
- 16kHz resample → 128-band log-Mel spectrogram

## Security
- SHA-256 (content hashing)
- HMAC-SHA256 (signing/verification, server-side secret only, never sent to frontend)
- DCT-domain watermarking (8×8 blocks, mid-frequency coefficients, redundant embedding + majority-vote extraction)

## API Endpoints

### `POST /api/detect/image`
- **Purpose:** Run deepfake detection on a single image.
- **Request:** `multipart/form-data`, field `file` (image).
- **Response:** `DetectionResult` (image variant) — verdict, probability, list of `FaceDetectionResult`, Grad-CAM reference(s).
- **Validation:** MIME/type/size check; must contain a decodable image.
- **Errors:** `400` invalid file, `413` too large, `422` unreadable/corrupted, `500` inference failure.
- **Auth:** None (MVP).

### `POST /api/detect/video`
- **Purpose:** Run deepfake detection on a video.
- **Request:** `multipart/form-data`, field `file` (video).
- **Response:** `DetectionResult` (video variant) — aggregate verdict/probability (per the `0.6·mean + 0.4·max` formula), list of `FramePrediction`.
- **Validation:** MIME/type/size/duration check; must be decodable by the video backend.
- **Errors:** `400/413/422/500` as above; `422` also covers "no faces found in any frame."
- **Auth:** None.

### `POST /api/detect/audio`
- **Purpose:** Run synthetic-audio detection.
- **Request:** `multipart/form-data`, field `file` (audio).
- **Response:** `AudioPrediction` — verdict (Real/Synthetic), probability.
- **Validation:** MIME/type/size/sample-readability check.
- **Errors:** `400/413/422/500`.
- **Auth:** None.

### `GET /api/detect/gradcam/{result_id}` *(or embedded inline in the detect response — see `[NEEDS CLARIFICATION]` in Schema.md)*
- **Purpose:** Retrieve Grad-CAM overlay image(s) for a prior detection result.
- **Response:** `GradCAMResult` (image reference/base64 + metadata).
- **Errors:** `404` unknown result id.
- **Auth:** None.

### `POST /api/authenticate/image`
- **Purpose:** Generate content ID + hash, embed watermark, sign.
- **Request:** `multipart/form-data`, field `file` (image).
- **Response:** `AuthenticationResult` (content ID, hash, watermarked image download reference — signature itself is server-stored, never returned raw).
- **Validation:** MIME/type/size; must support DCT embedding (min. dimensions for 8×8 blocks).
- **Errors:** `400/413/422/500`.
- **Auth:** None.

### `POST /api/verify/image`
- **Purpose:** Verify a submitted image against authentication records.
- **Request:** `multipart/form-data`, field `file` (image).
- **Response:** One of: `verified_original`, `tampered_after_signing`, `invalid_signature`, `no_watermark_found`, each with supporting metadata (content ID if recovered, hash comparison).
- **Validation:** MIME/type/size.
- **Errors:** `400/413/422/500`.
- **Auth:** None.

## Security
- **Input validation:** type, MIME (via content sniffing, not just extension), size, corruption checks on every upload endpoint.
- **File security:** randomized server-side filenames, no path-traversal-vulnerable naming, files processed in an isolated temp directory and cleaned up after use.
- **Secret management:** HMAC key from environment/secret store, never logged, never returned in any API response.
- **Cryptographic security:** SHA-256 + HMAC-SHA256 only; no custom crypto.
- **Data protection:** authentication records (hash + content ID + signature) are the only persisted authentication data — no raw image retained beyond what's needed to serve verification, unless product decides otherwise (`[NEEDS CLARIFICATION]`, see Schema.md).
- **Resource limits:** max upload size per media type, request timeouts, frame-extraction caps for very long videos.
- **Error handling:** consistent JSON error shape (`{ "error": { "code", "message" } }`), no stack traces leaked to the client.
