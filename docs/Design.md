# Design System — DeepGuard

## Design Direction
- **Visual personality:** precise, restrained, evidentiary — like a lab report, not a marketing page.
- **Brand personality:** trustworthy, technical, calm under uncertainty.
- **Mood:** analytical, quiet confidence — never hype.
- **Density:** information-dense but never cluttered; every data point earns its place.
- **Target audience:** journalists, researchers, creators, forensics learners — comfortable with technical detail, allergic to gimmicks.
- **Design references (principles, not literal copies):** scientific paper layouts, forensic lab reports, technical documentation sites (e.g., Stripe docs' typographic discipline), evidence-board layouts. Translate structure and restraint, not literal visuals.
- **Explicitly avoid:** generic AI-SaaS gradients/glassmorphism, crypto-dashboard neon, sci-fi HUDs, admin-panel templates.

## Visual Hierarchy
- **Primary focus:** the verdict (Real/Fake/Synthetic) and its confidence.
- **Secondary:** the evidence that supports it (face crops, frame table, spectrogram, Grad-CAM).
- **Supporting:** processing metadata (file info, timing, model version).
- **Primary action:** upload / run detection or authentication.
- **Secondary actions:** re-run, download report, verify another file.
- **Evidence hierarchy:** verdict → aggregate probability → per-unit (face/frame) breakdown → raw visual evidence. Never show evidence before the verdict it supports.

## Typography
- **Primary/body font:** a neutral, highly legible sans-serif (e.g., Inter or IBM Plex Sans).
- **Heading font:** same family, heavier weights — no separate display face; DeepGuard's identity comes from restraint, not display type.
- **Monospace font:** used selectively for hashes, content IDs, signatures, timestamps, and raw probability values (e.g., IBM Plex Mono or JetBrains Mono).
- **Rules:** limit to ~5 type sizes total; consistent line-height (1.4–1.6 for body); control text measure (~65–80ch max); weight (not size) carries most emphasis; no oversized hero text.

## Color
Restrained neutral palette; color is reserved for state communication only.
- **Primary:** deep slate/graphite (near-black, not pure black)
- **Secondary:** muted steel blue (used sparingly for links/focus)
- **Background:** off-white (light mode) / near-black graphite (dark mode)
- **Surface:** one step lighter/darker than background, minimal elevation via border not shadow
- **Text:** high-contrast graphite/off-white; muted variant for secondary text
- **Success / Real-Authentic:** muted forest green
- **Warning / Tampered:** amber
- **Error / Fake-Manipulated:** muted red (desaturated, not alarmist)
- **Synthetic audio state:** distinct violet-gray (visually distinguishable from "fake" red, since audio synthesis ≠ image manipulation)
- **Invalid/forged signature:** dark red, paired with an icon (not color alone)
- **No watermark found:** neutral gray (this is a "no data" state, not an error state)

All state colors must meet WCAG AA contrast and are always paired with an icon/label — never color alone.

## Spacing
Baseline scale (px): 4, 8, 12, 16, 24, 32, 48, 64, 96. No arbitrary values outside this scale.

## Layout
- **Max content width:** ~1200px for dashboards/results, ~760px for text-heavy docs/reports.
- **Grid:** 12-column on desktop, 4-column on mobile; consistent gutters (16–24px).
- **Section spacing:** 48–96px between major sections; 16–24px within a component group.
- **Alignment:** left-aligned text by default; numeric/technical tables right-aligned or monospaced-tabular.
- **Responsive breakpoints:** mobile (<640px), tablet (640–1024px), desktop (1024px+), large (1440px+).

## Result-State Visual Language
Distinct, accessible treatment for: Real/Authentic, Fake/Manipulated, Synthetic Audio, Tampered, Invalid Signature, No Watermark. Each state = icon + label + color (never color alone), consistently applied across image/video/audio/authentication result cards.

## Motion
Functional only: upload progress, processing spinners/steps, state-change transitions, focus/press feedback. Subtle and fast (150–250ms). Respect `prefers-reduced-motion`. No decorative animation.

## Accessibility
Semantic HTML, full keyboard navigation, visible focus rings, proper labels/ARIA, AA contrast minimum, accessible touch targets (≥44px), non-color-only state indicators, meaningful error text.

## Anti-Slop Checklist (apply before calling any screen "done")
No generic SaaS gradients, no glassmorphism, no oversized decorative headings, no excessive rounded cards/shadows, no badges without meaning, no fake metrics/status, no components that exist only because they were easy to generate.
