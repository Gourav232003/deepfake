import { useState } from "react";
import UploadDropzone from "../components/UploadDropzone.jsx";
import { authenticateImage } from "../api/client.js";

export default function AuthenticatePage() {
  const [status, setStatus] = useState("empty");
  const [result, setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  async function handleFile(file) {
    setStatus("loading");
    try {
      const data = await authenticateImage(file);
      setResult(data);
      setStatus("success");
    } catch (err) {
      setErrorMessage(err.message);
      setStatus("error");
    }
  }

  function downloadWatermarked() {
    const bytes = Uint8Array.from(result.watermarked_image_base64.match(/.{1,2}/g).map((b) => parseInt(b, 16)));
    const blob = new Blob([bytes], { type: "image/png" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `deepguard-authenticated-${result.content_id}.png`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="mx-auto max-w-content px-6 py-16">
      <h1 className="text-2xl font-semibold text-graphite-900">Authenticate Image</h1>
      <p className="mt-2 max-w-prose text-graphite-500">
        Embeds an invisible watermark and signs the image so you can later verify whether a copy
        has been altered.
      </p>

      <div className="mt-8">
        <UploadDropzone
          accept="image/jpeg,image/png,image/webp"
          label="Drop an original image to authenticate"
          onFileSelected={handleFile}
        />
      </div>

      {status === "loading" && <p className="mt-6 text-graphite-500">Embedding and signing…</p>}
      {status === "error" && <p className="mt-6 text-state-fake">{errorMessage}</p>}

      {status === "success" && result && (
        <div className="mt-8 space-y-3 rounded border border-graphite-300 p-6">
          <p className="text-sm text-graphite-500">Content ID</p>
          <p className="break-all font-mono text-sm text-graphite-900">{result.content_id}</p>
          <p className="mt-3 text-sm text-graphite-500">SHA-256</p>
          <p className="break-all font-mono text-xs text-graphite-500">{result.sha256_hash}</p>
          <button
            onClick={downloadWatermarked}
            className="mt-4 rounded bg-graphite-900 px-4 py-2 text-sm font-medium text-white hover:bg-graphite-700"
          >
            Download authenticated image
          </button>
        </div>
      )}
    </div>
  );
}
