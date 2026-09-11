# DEVELOPMENT RULES

## Engineering Rules
- Use clean, maintainable code.
- Follow existing project conventions.
- Prefer simple solutions over clever ones.
- Avoid unnecessary dependencies.
- Reuse components; avoid duplicated logic.
- Keep functions focused and components reasonably small.
- Do not rewrite working code unnecessarily.
- Do not modify unrelated files.
- Never remove functionality without approval.
- Never fabricate functionality, model performance, API responses, datasets, or evaluation results.

## AI Coding Rules
Before coding any phase, read in order:
1. PRD.md
2. Rules.md (this file)
3. Design.md
4. AppFlow.md
5. TechSpec.md
6. Schema.md
7. ImplementationPlan.md
8. Tracker.md

Never code blindly. If requirements conflict: **STOP**, explain the conflict, and mark it `[NEEDS CLARIFICATION]` rather than silently choosing.

## AI / Security Safety Rules
Never:
- Expose HMAC keys or any cryptographic secret to the frontend
- Hardcode production secrets
- Trust uploaded filenames or extensions alone (validate MIME + content)
- Claim fake accuracy numbers or fabricate evaluation results
- Present Grad-CAM as definitive forensic proof
- Claim universal deepfake-detection accuracy
- Add unnecessary authentication, databases, cloud services, or infrastructure

Always clearly distinguish **model prediction** from **forensic certainty** in every user-facing result.

## Documentation Consistency Rule
PRD → Rules → Design → AppFlow → TechSpec → Schema → ImplementationPlan → Tracker form a single source of truth. If one changes, check the others for drift before continuing implementation.
