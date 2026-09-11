import { useCallback, useState } from "react";

export default function UploadDropzone({ accept, onFileSelected, label }) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrop = useCallback(
    (event) => {
      event.preventDefault();
      setIsDragging(false);
      const file = event.dataTransfer.files?.[0];
      if (file) onFileSelected(file);
    },
    [onFileSelected]
  );

  return (
    <div
      role="button"
      tabIndex={0}
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") document.getElementById("file-input").click();
      }}
      className={`flex flex-col items-center justify-center rounded border-2 border-dashed p-12 text-center transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-graphite-700 ${
        isDragging ? "border-graphite-700 bg-graphite-100" : "border-graphite-300"
      }`}
    >
      <p className="mb-4 text-graphite-700">{label}</p>
      <input
        id="file-input"
        type="file"
        accept={accept}
        className="hidden"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) onFileSelected(file);
        }}
      />
      <label
        htmlFor="file-input"
        className="cursor-pointer rounded bg-graphite-900 px-4 py-2 text-sm font-medium text-white hover:bg-graphite-700"
      >
        Choose file
      </label>
      <p className="mt-3 text-xs text-graphite-500">or drag and drop</p>
    </div>
  );
}
