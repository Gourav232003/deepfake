# AppFlow — DeepGuard

High-level journey:

Landing → Choose Operation → Upload Media → Validate → Process → Result → Evidence/Explainability → Next Action

All routes below are public (no `[NEEDS CLARIFICATION]`-resolved auth system exists for MVP — see Rules.md / Schema.md).

---

## Screen: Landing / Home
**Purpose:** Explain what DeepGuard does and route to an operation; set expectations about ML limitations up front.
**Entry:** Direct visit.
**Primary Action:** Choose an operation (Detect Image / Video / Audio, Authenticate Image, Verify Image).
**Secondary Actions:** Learn more / methodology link.
**Navigation:** → Upload Media (per chosen operation).
**States:** Success only (static content); no loading/error states.
**Authentication:** Not required.

## Screen: Upload Media
**Purpose:** Accept a file for the chosen operation.
**Entry:** From Landing (operation chosen) or direct deep link.
**Primary Action:** Select/drag file, submit.
**Secondary Actions:** Change operation, cancel.
**Navigation:** → Processing (on valid submit) or stays with inline error (on invalid file).
**States:**
- Empty: no file selected yet, drop-zone visible.
- Loading: file validating (client-side checks) before submit.
- Error: wrong type/size/corrupted file — specific, actionable message.
- Success: file accepted, transitions to Processing.
**Authentication:** Not required.

## Screen: Processing
**Purpose:** Show real progress while the backend runs detection/authentication.
**Entry:** From Upload Media after a valid submit.
**Primary Action:** None (wait); Cancel where technically feasible.
**Navigation:** → Result (on completion) or → Error state (on backend failure).
**States:**
- Loading: staged progress (e.g., "validating," "extracting frames," "running model," "generating evidence").
- Error: backend/model failure, corrupted-after-upload, timeout.
**Authentication:** Not required.

## Screen: Result — Image Detection
**Purpose:** Present verdict + evidence for an image.
**Primary Action:** View Grad-CAM / face-level detail.
**Secondary Actions:** Run another detection, download report.
**Navigation:** → Evidence panel (in-page), → Upload Media (new run).
**States:** Success (0 faces / 1 face / multiple faces handled distinctly), Error (model failure).
**Authentication:** Not required.

## Screen: Result — Video Detection
**Purpose:** Present aggregate verdict + frame-level table/timeline.
**Primary Action:** Inspect frame-level evidence (table or timeline scrub).
**Secondary Actions:** Run another detection, download report.
**Navigation:** → Frame detail (in-page expand), → Upload Media.
**States:** Success, Empty (no faces detected in any frame — explicit message, not a silent Fake/Real guess), Error.
**Authentication:** Not required.

## Screen: Result — Audio Detection
**Purpose:** Present Real/Synthetic verdict with spectrogram context.
**Primary Action:** View spectrogram / confidence detail.
**Secondary Actions:** Run another detection, download report.
**Navigation:** → Upload Media.
**States:** Success, Error (unsupported/corrupted audio).
**Authentication:** Not required.

## Screen: Authenticate Image
**Purpose:** Generate content ID, hash, watermark, and signature for an original image.
**Primary Action:** Upload → Authenticate.
**Secondary Actions:** Download authenticated copy + certificate (content ID/hash/signature reference).
**Navigation:** → Confirmation screen with content ID.
**States:** Loading (embedding/signing), Error (embedding failure, unsupported format), Success.
**Authentication:** Not required (no user accounts in MVP; content ID is the retrieval key — see Schema.md `[NEEDS CLARIFICATION]` on persistence).

## Screen: Verify Image
**Purpose:** Check an image against its authentication record.
**Primary Action:** Upload → Verify.
**Secondary Actions:** Run another verification.
**Navigation:** → Result: exactly one of Verified Original / Tampered After Signing / Invalid-Forged Signature / No Recognized Watermark.
**States:** Loading (extraction/verification), Error (unreadable file), Success (one of the four states above — never collapsed to Verified/Not Verified).
**Authentication:** Not required.

---

## Edge Cases & Failure Journeys
- Invalid file type/extension mismatch → reject at Upload with specific message, no processing attempted.
- Oversized file → reject before upload completes.
- Corrupted file that passes initial validation → fail during Processing with a clear, non-technical error and a retry option.
- Image with zero detected faces → explicit "no face detected" result, not a forced Real/Fake verdict.
- Video with faces in only some frames → aggregate only over frames with valid face detections; state this in the result.
- Watermark extraction with low-confidence majority vote → surfaces as "No Recognized Watermark," not a false "Verified."
- Tampered-but-signed image → must resolve to "Tampered After Signing," never silently pass as Verified.
