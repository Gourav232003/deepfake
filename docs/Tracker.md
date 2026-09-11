# Project Tracker — DeepGuard

## To Do
- [ ] Resolve `[NEEDS CLARIFICATION]` items in ImplementationPlan.md (Phase 3)
- [ ] Scaffold frontend (Vite + React + Tailwind)
- [ ] Scaffold backend (Flask blueprints)
- [ ] File validation layer
- [ ] Image detection pipeline (face detect → classify → Grad-CAM)
- [ ] Video detection pipeline + aggregation
- [ ] Audio detection pipeline
- [ ] Authentication (watermark + signing)
- [ ] Verification (4-state logic)
- [ ] Integration across frontend/backend
- [ ] Testing suite
- [ ] Design polish pass
- [ ] Evaluation on real benchmark data

## In Progress
- [ ] Phase 1–2: Discovery & Product Blueprint (this document set)

## Completed
*(nothing implemented yet — planning only)*

---

## Categories

### Product
- [ ] PRD validated against actual build decisions

### Design
- [ ] Design.md system implemented in Tailwind config/tokens
- [ ] Anti-slop critique pass completed on each screen

### Frontend
- [ ] Upload flow (image/video/audio)
- [ ] Result screens (image/video/audio)
- [ ] Authenticate/Verify screens

### Backend
- [ ] Flask blueprints + routing
- [ ] File validation utilities

### AI/ML
- [ ] EfficientNet-B0 wiring (pending model-provenance clarification)
- [ ] Audio CNN+BiLSTM wiring
- [ ] Grad-CAM implementation

### Computer Vision
- [ ] Face detection chain (DNN → Haar → center-crop)

### Audio
- [ ] Resampling + log-Mel pipeline

### Security
- [ ] Secret management (HMAC key never exposed)
- [ ] Upload validation/hardening

### Authentication
- [ ] DCT watermark embed/extract
- [ ] SHA-256 + HMAC-SHA256 sign/verify
- [ ] 4-state verification logic

### Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] Security tests

### Deployment
- [ ] Not started — pending scope clarification (see ImplementationPlan.md item 5)

**Rule:** nothing gets moved to Completed unless it actually works and has been verified.
