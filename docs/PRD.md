# Product Requirements Document

## Product Name
DeepGuard — DeepFake Detection & Content Authentication System

## Product Vision
Build an explainable AI-powered platform for detecting manipulated images, videos, and synthetic audio, while providing image authentication through invisible watermarking and cryptographic signing.

## Problem Statement
Deepfake detection tools usually expose a bare probability ("Fake — 92%") with no supporting evidence, which is hard to trust or act on. Separately, creators have no lightweight way to prove an image is theirs and later detect whether it's been altered. DeepGuard addresses both: explainable detection evidence (face crops, frame breakdowns, Grad-CAM attention) and a content-authentication workflow (watermark + cryptographic signature + tamper detection).

## Target Users
- General users verifying suspicious media
- Content creators
- Journalists
- Researchers
- Digital media reviewers
- Cybersecurity / digital-forensics learners
- Organizations performing media verification
- Academic/research users studying deepfake detection

## User Personas
1. **The Verifier (journalist/general user)** — receives a suspicious clip or image, needs a fast, evidence-backed verdict they can act on or cite.
2. **The Creator** — wants to authenticate original images before publishing so later edits/reuploads can be checked.
3. **The Researcher/Learner** — wants to inspect frame-level and Grad-CAM detail to understand *why* a model reached a verdict, not just the verdict.

## Goals
- Detect manipulated images
- Detect manipulated videos
- Detect synthetic audio
- Provide explainability (Grad-CAM, face/frame evidence)
- Authenticate original images (watermark + signature)
- Detect post-signing tampering
- Provide cryptographic verification
- Present clear, forensic-oriented results with honest limitations

## Core Features
1. Image deepfake detection (face detect → crop/align → 224×224 → classify → Grad-CAM)
2. Video deepfake detection (frame extraction → per-frame face detect/classify → weighted aggregation `0.6·mean + 0.4·max`)
3. Audio deepfake detection (16kHz resample → 128-band log-Mel → CNN + 2-layer BiLSTM → classify)
4. Explainable AI (Grad-CAM overlays, framed as "model attention," not forensic proof)
5. Image authentication (content ID, hash, DCT watermark, redundant embedding)
6. Cryptographic signing (SHA-256 + HMAC-SHA256, server-side secret only)
7. Authentication verification with four distinct states (Verified / Tampered / Invalid-Forged / No Watermark)

## User Stories
- As a **general user**, I want to upload a suspicious image and see a Real/Fake verdict with visual evidence, so that I can judge its credibility myself rather than trust a bare score.
- As a **journalist**, I want to inspect frame-level predictions in a video, so that I can identify exactly which segments look manipulated.
- As a **creator**, I want to authenticate my original image before publishing, so that I can later prove whether a copy has been altered.
- As a **researcher**, I want to see the Grad-CAM heatmap and know its limitations, so that I don't overstate the model's certainty.
- As any user, I want clear error messages on invalid/corrupted uploads, so that I understand why processing failed.

## Success Criteria
- Every detection result surfaces at minimum: verdict, probability, and at least one piece of supporting evidence (face crop, frame table, or spectrogram/attention view).
- Video verdict uses the specified aggregation formula and never a silently substituted one.
- No cryptographic secret is ever present in any frontend-bound payload (verified via code review/tests, not just intent).
- Authentication verification always returns exactly one of the four defined states — never a collapsed binary.
- Reported model metrics (accuracy/precision/recall/F1/ROC-AUC, EER for audio) come only from actual evaluation runs on real data — never fabricated.

## Out of Scope (MVP)
- Real-time live-stream analysis
- Mobile-device deployment
- Video watermarking
- Audio watermarking
- User accounts / persistent profiles / payments (no requirement stated — see Rules.md / [NEEDS CLARIFICATION])

## Future Features
- Video watermarking
- Audio watermarking
- Additional model architectures
- Additional authentication workflows (e.g., video/audio content IDs)

## Open Items
See the `[NEEDS CLARIFICATION]` list in `ImplementationPlan.md` — most materially: whether real model *training* on FaceForensics++/Celeb-DF/DFDC/ASVspoof is in scope for this engagement, or whether the MVP ships with a pretrained/placeholder inference model behind the same interfaces.
