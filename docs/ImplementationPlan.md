# Implementation Plan — DeepGuard

Built incrementally; the entire application is not generated in one step. Each phase is completed, tested, and design-reviewed (where applicable) before moving to the next.

## Phase 1 — Discovery ✅ (this document set)
- [x] Understand project
- [x] Identify requirements, users, journeys, feature boundaries
- [x] Identify ambiguities (see `[NEEDS CLARIFICATION]` list below)

## Phase 2 — Product Blueprint ✅
- [x] PRD.md, Rules.md, Design.md, AppFlow.md, TechSpec.md, Schema.md, ImplementationPlan.md, Tracker.md created

## Phase 3 — Blueprint Validation
- [ ] Confirm no contradictions across the eight docs
- [ ] Resolve `[NEEDS CLARIFICATION]` items below before Phase 4 begins in earnest

## Phase 4 — Foundation
- [ ] Repo/project structure (frontend + backend)
- [ ] Vite React app scaffold, Tailwind configured
- [ ] Flask app scaffold with blueprints (`detect`, `authenticate`, `verify`)
- [ ] Shared config (env vars, upload limits)
- [ ] File validation layer (type/MIME/size/corruption)
- [ ] Consistent error-response envelope

## Phase 5 — Image Detection
- [ ] Face detection (OpenCV DNN → Haar → center-crop fallback chain)
- [ ] Face preprocessing (crop/align/resize 224×224)
- [ ] EfficientNet-B0 inference wiring (pretrained or placeholder — see clarification)
- [ ] Prediction result assembly (`DetectionResult` + `FaceDetectionResult`)
- [ ] Grad-CAM generation
- [ ] Image result UI (verdict, per-face evidence, Grad-CAM overlay)

## Phase 6 — Video Detection
- [ ] Video validation + frame extraction
- [ ] Per-frame face detection/classification (reuses Phase 5 pipeline)
- [ ] Frame-level result storage (`FramePrediction`)
- [ ] Aggregation: `0.6 × mean(frame probabilities) + 0.4 × max(frame probability)`
- [ ] Video result UI (aggregate verdict + frame table/timeline)
- [ ] Explainability surfaced per frame where applicable

## Phase 7 — Audio Detection
- [ ] Audio validation
- [ ] 16kHz resampling
- [ ] 128-band log-Mel spectrogram generation
- [ ] CNN + 2-layer BiLSTM model wiring
- [ ] Classification + `AudioPrediction` assembly
- [ ] Audio result UI (verdict, spectrogram view)

## Phase 8 — Authentication
- [ ] Content ID generation
- [ ] SHA-256 hashing
- [ ] DCT watermarking (8×8 blocks, mid-frequency, redundant embedding)
- [ ] Majority-voting extraction
- [ ] HMAC-SHA256 signing (server-side secret)
- [ ] Verification logic returning the 4 distinct states
- [ ] Tamper detection
- [ ] Authenticate/Verify UI

## Phase 9 — Integration
- [ ] Frontend/API wiring for all endpoints
- [ ] Loading/error/empty/result states across all flows
- [ ] Explainability + authentication surfaced consistently in UI

## Phase 10 — Testing
- [ ] Unit tests (validation, hashing, watermark embed/extract, aggregation formula)
- [ ] Integration tests (end-to-end per endpoint)
- [ ] Model inference tests (shape/output sanity, not accuracy claims)
- [ ] Upload validation tests (bad type, oversized, corrupted)
- [ ] Authentication/watermark round-trip tests (embed→extract→verify, including tampered case)
- [ ] Security tests (secret never in response payloads, path traversal, oversized/resource exhaustion)
- [ ] Responsive + accessibility tests

## Phase 11 — Design Polish
- [ ] Visual hierarchy / typography / spacing pass
- [ ] Responsive pass (mobile frame tables, evidence panels)
- [ ] Micro-interactions (upload, processing, verification states)
- [ ] Accessibility pass
- [ ] Design critique against Design.md's anti-slop checklist
- [ ] Iterate

## Phase 12 — Evaluation
- [ ] Compute accuracy/precision/recall/F1/ROC-AUC on real benchmark data
- [ ] Compute EER for audio
- [ ] Confusion matrix, class distribution, per-class metrics
- [ ] Document dataset(s) actually used for train/val/test — no fabricated numbers

## Phase 13 — Deployment (only if actually required)
- [ ] Environment configuration
- [ ] Production build
- [ ] Secure secrets management
- [ ] Production testing
- [ ] Deployment documentation

---

## `[NEEDS CLARIFICATION]` — Must Resolve Before Deep Implementation

1. **Model provenance (highest impact):** Does this engagement include actually *training* EfficientNet-B0 / the audio CNN+BiLSTM on FaceForensics++, Celeb-DF, DFDC, and ASVspoof? That is a substantial undertaking on its own (dataset access/licensing, GPU training time, days-to-weeks of work) — separate from building the application around it. Alternative: ship the MVP with the full pipeline wired to a pretrained/placeholder model (clearly labeled as such) so the product is demonstrable end-to-end, and treat real training as a distinct, later effort. **This decision changes the shape of Phase 5–7 and Phase 12 significantly.**
2. **Dataset splits/preprocessing protocol:** If training is in scope, exact train/val/test splits and preprocessing steps aren't specified and shouldn't be invented silently.
3. **Persistence for authentication/verification:** self-contained-in-the-watermark (no DB) vs. a lightweight lookup store — see Schema.md.
4. **Media retention policy:** are uploaded files deleted immediately post-processing, kept for the session, or never persisted?
5. **Deployment target:** is Phase 13 in scope at all for this engagement, or is DeepGuard a local/demo-only build?
6. **Grad-CAM delivery:** inline in the detect response vs. a separate `/gradcam/{id}` fetch (affects Schema.md's result-id lifecycle).

None of these block Phases 1–4 (foundation/scaffolding), but items 1–2 materially block real Phase 5–7 model work, and item 3 blocks Phase 8.
