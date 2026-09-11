/**
 * Centralized API client. Every DeepGuard backend call goes through here so
 * error handling and the response envelope are handled in exactly one place.
 */
const BASE_URL = "/api";

async function postFile(path, file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    body: formData,
  });

  const body = await response.json();

  if (!response.ok || body.success === false) {
    const message = body?.error?.message || "Something went wrong.";
    throw new Error(message);
  }

  return body.data;
}

export const detectImage = (file) => postFile("/detect/image", file);
export const detectVideo = (file) => postFile("/detect/video", file);
export const detectAudio = (file) => postFile("/detect/audio", file);
export const authenticateImage = (file) => postFile("/authenticate/image", file);
export const verifyImage = (file) => postFile("/verify/image", file);
