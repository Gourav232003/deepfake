# DeepGuard — Phase 4 Foundation Scaffold

This is the Phase 4 ("Foundation") output from `ImplementationPlan.md`. It is a working
skeleton, not a finished product — see each doc in `/docs` for the full plan.

## What's actually wired up

- **Backend (`/backend`)**: Flask app factory, blueprints for `detect`, `authenticate`,
  `verify`; file validation (real MIME sniffing, size limits); the full image-detection
  pipeline (face detection with DNN→Haar→center-crop fallback, EfficientNet-B0 inference,
  fixed video aggregation formula defined and unit-testable); DCT watermark embed/extract;
  SHA-256 + HMAC-SHA256 sign/verify; the four-state verification response.
- **Frontend (`/frontend`)**: Vite + React + Tailwind, routed pages for Detect
  (image/video/audio), Authenticate, and Verify, a shared API client, and a `StateBadge`
  component that follows Design.md's "never color alone" rule.

## What's intentionally a placeholder (see `ImplementationPlan.md`)

- **The image classifier is untrained** (`backend/app/services/inference.py`). It runs a
  real EfficientNet-B0 forward pass so the full pipeline is demonstrable, but every result
  is labeled as a placeholder. Swap in real trained weights before treating any output as
  a real accuracy claim — do not remove that label until you do.
- **Video and audio detection endpoints validate uploads but raise "not yet implemented"**
  (Phase 6 / Phase 7 work) — the aggregation formula and audio-pipeline shape are defined
  and ready to wire in.
- **Grad-CAM is not yet implemented** (Phase 5 remainder).
- **Authentication persistence** uses a plain JSON file (`auth_store.py`) as the smallest
  thing that makes the four verification states real. Replace with a proper store (or
  remove entirely if you decide watermark+signature should be fully self-contained) before
  this goes anywhere near production — see `Schema.md`'s open item.

## Running it

Backend:
```
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then set a real DEEPGUARD_HMAC_SECRET_KEY
python run.py
```

Frontend:
```
cd frontend
npm install
npm run dev
```

The Vite dev server proxies `/api` to `http://localhost:5000`, so both need to be running.
