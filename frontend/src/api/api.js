// src/api/analyzeApi.js
import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

export const analyzePlateImage = async (imageFile) => {
  const formData = new FormData();
  formData.append("image", imageFile); // ✅ must match backend upload.single("image")

  const response = await axios.post(`${API_BASE_URL}/api/analyze`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};