import axios from "axios";
import FormData from "form-data";
import fs from "fs";

const ML_SERVICE_URL =
  process.env.ML_SERVICE_URL ||
  "https://hardecomm-naijaplate.hf.space";

export async function analyzeWithML(
  filePath,
  refined = false
) {
  const form = new FormData();

  form.append(
    "file",
    fs.createReadStream(filePath)
  );

  const endpoint = refined
    ? "/analyze-refined"
    : "/analyze";

  console.log(
    "[ML SERVICE URL]",
    `${ML_SERVICE_URL}${endpoint}`
  );

  const response = await axios.post(
    `${ML_SERVICE_URL}${endpoint}`,
    form,
    {
      headers: form.getHeaders(),
      maxContentLength: Infinity,
      maxBodyLength: Infinity,
      timeout: 120000,
    }
  );

  return response.data;
}
