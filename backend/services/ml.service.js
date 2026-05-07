import axios from "axios";
import FormData from "form-data";
import fs from "fs";

const ML_SERVICE_URL =
  process.env.ML_SERVICE_URL || "http://127.0.0.1:7860";

export async function analyzeWithML(filePath, refined = false) {
  const form = new FormData();

  form.append("file", fs.createReadStream(filePath));

  const endpoint = refined
    ? "/analyze-refined"
    : "/analyze";

  const response = await axios.post(
    `${ML_SERVICE_URL}${endpoint}`,
    form,
    {
      headers: form.getHeaders(),
      maxContentLength: Infinity,
      maxBodyLength: Infinity,
    }
  );

  return response.data;
}