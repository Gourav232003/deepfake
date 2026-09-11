import { useState } from "react";
import UploadDropzone from "../components/UploadDropzone.jsx";
import StateBadge from "../components/StateBadge.jsx";
import { verifyImage } from "../api/client.js";

export default function VerifyPage() {
  const [status, setStatus] = useState("empty");
  const [result, setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  async function handleFile(file) {
    setStatus("loading");
    try {
      const data = await verifyImage(file);
      setResult(data);
      setStatus("success");
    } catch (err) {
      setErrorMessage(err.message);
      setStatus("error");
    }
  }

  return (
    <div className="mx-auto max-w-content px-6 py-16">
      <h1 className="text-2xl font-semibold text-graphite-900">Verify Image</h1>
      <p className="mt-2 max-w-prose text-graphite-500">
        Checks a submitted image against its authentication record, if one exists.
      </p>

      <div className="mt-8">
        <UploadDropzone
          accept="image/jpeg,image/png,image/webp"
          label="Drop an image to verify"
          onFileSelected={handleFile}
        />
      </div>

      {status === "loading" && <p className="mt-6 text-graphite-500">Checking watermark and signature…</p>}
      {status === "error" && <p className="mt-6 text-state-fake">{errorMessage}</p>}

      {status === "success" && result && (
        <div className="mt-8 space-y-3 rounded border border-graphite-300 p-6">
          <StateBadge status={result.status} />
          {result.content_id && (
            <p className="break-all font-mono text-xs text-graphite-500">content id: {result.content_id}</p>
          )}
        </div>
      )}
    </div>
  );
}
