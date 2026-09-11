/**
 * Renders a verdict/status as icon + label + color, per Design.md:
 * "never color alone" for state indicators.
 */
const STATE_MAP = {
  real: { label: "Real / Authentic", color: "bg-state-real", icon: "✓" },
  fake: { label: "Fake / Manipulated", color: "bg-state-fake", icon: "✕" },
  synthetic: { label: "Synthetic Audio", color: "bg-state-synthetic", icon: "◆" },
  tampered_after_signing: { label: "Tampered After Signing", color: "bg-state-tampered", icon: "!" },
  invalid_signature: { label: "Invalid / Forged Signature", color: "bg-state-invalid", icon: "✕" },
  no_watermark_found: { label: "No Recognized Watermark", color: "bg-state-nowatermark", icon: "–" },
  verified_original: { label: "Verified Original", color: "bg-state-real", icon: "✓" },
  no_face_detected: { label: "No Face Detected", color: "bg-state-nowatermark", icon: "–" },
};

export default function StateBadge({ status }) {
  const entry = STATE_MAP[status] || { label: status, color: "bg-graphite-500", icon: "•" };
  return (
    <span
      className={`inline-flex items-center gap-2 rounded px-3 py-1 text-sm font-medium text-white ${entry.color}`}
    >
      <span aria-hidden="true">{entry.icon}</span>
      {entry.label}
    </span>
  );
}
