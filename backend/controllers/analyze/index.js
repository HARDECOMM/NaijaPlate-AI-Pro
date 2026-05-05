import fs from "fs";
import { PYTHON_PATH, PYTHON_MAIN } from "../../config/paths.js";
import { runPython } from "../../utils/spawnPython.js";

export const analyzeFile = async (req, res) => {
  let filePath;

  try {
    if (!req.file) {
      return res.status(400).json({
        error: "No file uploaded. Use form-data key: file",
      });
    }

    filePath = req.file.path;

    const mimeType = req.file.mimetype;
    const isVideo = mimeType.startsWith("video/");
    const mode = isVideo ? "video" : "image";

    console.log(`[API] ${mode} received:`, filePath);
    console.log("[DEBUG] PYTHON_PATH:", PYTHON_PATH);
    console.log("[DEBUG] PYTHON_MAIN:", PYTHON_MAIN);

    if (!fs.existsSync(PYTHON_MAIN)) {
      return res.status(500).json({
        error: "Python main.py not found",
        path: PYTHON_MAIN,
      });
    }

    const args = isVideo
      ? [PYTHON_MAIN, filePath, "--video", "--json"]
      : [PYTHON_MAIN, filePath, "--json"];

    const result = await runPython(PYTHON_PATH, args);

    console.log("[PYTHON OUTPUT]");
    console.log(result);

    let json;

    try {
      json = JSON.parse(result);
    } catch {
      return res.status(500).json({
        error: "Invalid JSON from Python",
        raw: result,
      });
    }

    return res.json({
      status: "success",
      mode,
      data: json,
    });
  } catch (err) {
    console.error("[SERVER ERROR]", err);

    return res.status(500).json({
      error: err.message || err.toString(),
      details: "Backend failed during Python/ML processing. Check Render logs.",
    });
  } finally {
    if (filePath && fs.existsSync(filePath)) {
      try {
        fs.unlinkSync(filePath);
      } catch {}
    }
  }
};