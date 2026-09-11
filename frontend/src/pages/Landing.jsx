import { Link } from "react-router-dom";

const OPERATIONS = [
  { to: "/detect/image", title: "Detect Image", description: "Check a photo for signs of face manipulation." },
  { to: "/detect/video", title: "Detect Video", description: "Check a video, frame by frame, for manipulated faces." },
  { to: "/detect/audio", title: "Detect Audio", description: "Check a clip for signs of synthetic or cloned speech." },
  { to: "/authenticate", title: "Authenticate Image", description: "Sign an original image so later copies can be checked." },
  { to: "/verify", title: "Verify Image", description: "Check whether an image matches its authentication record." },
];

export default function Landing() {
  return (
    <div className="mx-auto max-w-content px-6 py-16">
      <h1 className="max-w-prose text-3xl font-semibold text-graphite-900">
        Media authentication with visible reasoning
      </h1>
      <p className="mt-4 max-w-prose text-graphite-700">
        DeepGuard checks images, video, and audio for signs of manipulation and shows the
        evidence behind each verdict — not just a score. It also lets creators sign original
        images so later copies can be checked for tampering.
      </p>
      <p className="mt-4 max-w-prose text-sm text-graphite-500">
        Every result is a model prediction, not forensic proof. Accuracy depends on training
        data and will not catch every manipulation.
      </p>

      <div className="mt-12 grid grid-cols-1 gap-4 sm:grid-cols-2">
        {OPERATIONS.map((op) => (
          <Link
            key={op.to}
            to={op.to}
            className="rounded border border-graphite-300 p-5 hover:border-graphite-700"
          >
            <h2 className="font-medium text-graphite-900">{op.title}</h2>
            <p className="mt-1 text-sm text-graphite-500">{op.description}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
