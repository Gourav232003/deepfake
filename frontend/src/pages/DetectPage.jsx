import { useState } from "react";
import { useParams } from "react-router-dom";
import UploadDropzone from "../components/UploadDropzone.jsx";
import StateBadge from "../components/StateBadge.jsx";
import { detectImage, detectVideo, detectAudio } from "../api/client.js";

const CONFIG = {
  image: { accept: "image/jpeg,image/png,image/webp", label: "Drop an image to check", run: detectImage },
  video: { accept: "video/mp4,video/quicktime,video/x-matroska", label: "Drop a video to check", run: detectVideo },
  audio: { accept: "audio/wav,audio/mpeg,audio/flac", label: "Drop an audio clip to check", run: detectAudio },
};

export default function DetectPage() {
  const { mediaType } = useParams(); // "image" | "video" | "audio"
  const config = CONFIG[mediaType];

  const [status, setStatus] = useState("empty"); // empty | loading | error | success
  const [result, setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  async function handleFile(file) {
    setStatus("loading");
    setErrorMessage("");
    try {
      const data = await config.run(file);
      setResult(data);
      setStatus("success");
    } catch (err) {
      setErrorMessage(err.message);
      setStatus("error");
    }
  }

  if (!config) {
    return <p className="mx-auto max-w-content px-6 py-16 text-graphite-700">Unknown detection type.</p>;
  }

  return (
    <div className="mx-auto max-w-content px-6 py-16">
      <h1 className="text-2xl font-semibold capitalize text-graphite-900">Detect {mediaType}</h1>

      <div className="mt-8">
        <UploadDropzone accept={config.accept} label={config.label} onFileSelected={handleFile} />
      </div>

      {status === "loading" && <p className="mt-6 text-graphite-500">Processing…</p>}

      {status === "error" && (
        <p className="mt-6 rounded border border-state-fake/30 bg-state-fake/5 p-4 text-state-fake">
          {errorMessage}
        </p>
      )}

      {status === "success" && result && (
        <div className="mt-8 space-y-4 rounded border border-graphite-300 p-6">
          <StateBadge status={result.verdict} />
          {typeof result.probability === "number" && (
            <p className="font-mono text-sm text-graphite-500">
              probability: {result.probability.toFixed(3)}
            </p>
          )}
          {result.model_notice && <p className="text-sm text-graphite-500">{result.model_notice}</p>}
          <p className="text-sm text-graphite-500">{result.limitations_notice}</p>

          {result.evidence?.faces?.length > 0 && (
            <div>
              <h2 className="font-medium text-graphite-900">Face-level evidence</h2>
              <table className="mt-2 w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-graphite-300 text-graphite-500">
                    <th className="py-1">Face</th>
                    <th>Probability</th>
                    <th>Detector</th>
                  </tr>
                </thead>
                <tbody>
                  {result.evidence.faces.map((f) => (
                    <tr key={f.face_id} className="border-b border-graphite-100">
                      <td className="py-1">{f.face_id}</td>
                      <td className="font-mono">{f.probability.toFixed(3)}</td>
                      <td>{f.detector_used}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
