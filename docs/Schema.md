# Schema — DeepGuard

**Database is not required for the current MVP** for detection features (image/video/audio detection are stateless request→response operations).

Authentication/verification introduces one genuine persistence need: a verification lookup must later confirm whether a given image matches something previously authenticated. `[NEEDS CLARIFICATION]`: is this persisted in a lightweight store (e.g., SQLite/JSON file keyed by content ID) or is verification designed to be fully self-contained in the image itself (hash/content ID recoverable from the watermark + signature alone, no external lookup)? The DCT-watermark + HMAC design in TechSpec.md leans toward "self-contained" (everything needed to verify is recoverable from the image + a server-side secret), which would avoid a database — but this should be confirmed before Phase 8 implementation.

## Data Structures

### DetectionResult (shared shape, image/video/audio variants)
| Field | Type | Required | Description | Validation |
|---|---|---|---|---|
| result_id | string (uuid) | yes | Unique id for this run | server-generated |
| media_type | enum(image,video,audio) | yes | Which pipeline produced this | — |
| verdict | enum(real,fake,synthetic,no_face_detected) | yes | Top-level verdict | — |
| probability | float 0–1 | yes | Aggregate confidence | 0 ≤ x ≤ 1 |
| created_at | ISO8601 timestamp | yes | When processed | server-generated |
| evidence | object | yes | Type-specific evidence (see below) | — |
| limitations_notice | string | yes | Standard disclaimer text | non-empty |

### FaceDetectionResult (image)
| Field | Type | Required | Description | Validation |
|---|---|---|---|---|
| face_id | string | yes | Index/id within the image | unique per result |
| bounding_box | {x,y,w,h} | yes | Detected face location | within image bounds |
| probability | float 0–1 | yes | Per-face fake probability | 0 ≤ x ≤ 1 |
| gradcam_ref | string | no | Reference to GradCAMResult | — |
| detector_used | enum(dnn,haar,center_crop) | yes | Which detection method succeeded | — |

### FramePrediction (video)
| Field | Type | Required | Description | Validation |
|---|---|---|---|---|
| frame_index | int | yes | Position in video | ≥ 0 |
| timestamp_ms | int | yes | Time offset | ≥ 0 |
| faces | list[FaceDetectionResult] | yes | Faces found in this frame (may be empty) | — |
| frame_probability | float 0–1 | no | Max/representative face probability for the frame | present only if ≥1 face found |

### AudioPrediction
| Field | Type | Required | Description | Validation |
|---|---|---|---|---|
| verdict | enum(real,synthetic) | yes | Classification | — |
| probability | float 0–1 | yes | Confidence | 0 ≤ x ≤ 1 |
| duration_sec | float | yes | Clip length | > 0 |
| sample_rate_used | int | yes | Always 16000 post-resample | = 16000 |

### GradCAMResult
| Field | Type | Required | Description | Validation |
|---|---|---|---|---|
| gradcam_id | string | yes | Id | unique |
| overlay_image_ref | string | yes | Path/base64 of heatmap overlay | — |
| target_face_id or frame_index | string/int | yes | What this heatmap explains | must reference an existing face/frame |
| disclaimer | string | yes | "Model attention, not forensic proof" notice | non-empty |

### WatermarkMetadata
| Field | Type | Required | Description | Validation |
|---|---|---|---|---|
| content_id | string (uuid) | yes | Unique id embedded/associated | server-generated |
| embedding_method | string | yes | e.g. "dct-8x8-midfreq-redundant" | fixed value |
| block_size | int | yes | 8 | = 8 |
| created_at | timestamp | yes | — | — |

### AuthenticationResult
| Field | Type | Required | Description | Validation |
|---|---|---|---|---|
| content_id | string | yes | From WatermarkMetadata | — |
| sha256_hash | string | yes | Hash of original content | 64 hex chars |
| hmac_signature | string | no (server-only) | Never returned to client in raw form | server-side only |
| watermarked_image_ref | string | yes | Downloadable watermarked file | — |

### APIRequest / APIResponse (generic envelope)
| Field | Type | Required | Description |
|---|---|---|---|
| success | bool | yes | Whether the call succeeded |
| data | object | no | Payload on success |
| error | {code, message} | no | Populated on failure only |

## Open Items
- `[NEEDS CLARIFICATION]`: persistence approach for authentication/verification (see above).
- `[NEEDS CLARIFICATION]`: retention policy for uploaded media (deleted immediately after processing vs. kept for a session vs. never stored) — affects Security section of TechSpec.md.
