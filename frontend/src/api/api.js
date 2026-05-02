const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

export async function analyzePlate(file) {
  const formData = new FormData();
  formData.append("image", file);

  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: "POST",
    body: formData,
  });

  const text = await response.text();

  if (!text) {
    throw new Error(`Backend returned empty response. Status: ${response.status}`);
  }

  let data;

  try {
    data = JSON.parse(text);
  } catch {
    throw new Error(`Backend returned non-JSON response. Status: ${response.status}`);
  }

  if (!response.ok) {
    throw new Error(data?.error || `Request failed with status ${response.status}`);
  }

  return data;
}