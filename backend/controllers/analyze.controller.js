import fs from "fs";
import { PYTHON_PATH, PYTHON_MAIN } from "../config/paths.js";
import { runPython } from "../utils/spawnPython.js";

export const analyzeImage = async (req, res) => {
  let filePath;

  try {
    if (!req.file) {
      return res.status(400).json({
        error: "No image uploaded. Use form-data key: image",
      });
    }

    filePath = req.file.path;

    if (!fs.existsSync(PYTHON_MAIN)) {
      return res.status(500).json({
        error: "Python main.py not found",
        path: PYTHON_MAIN,
      });
    }

    const result = await runPython(PYTHON_PATH, [
      PYTHON_MAIN,
      filePath,
      "--json",
    ]);

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
      data: {
        plate: json.plate,
        state: json.state,
        nickname: json.nickname,
        confidence: json.confidence,
        annotated_detection_url: json.annotated_detection_url || null,
        crop_url: json.crop_url || null,
        processed_url: json.processed_url || null,
        result_url: json.result_url || null,
        ...(json.error && { error: json.error }),
      },
    });
  } catch (err) {
    return res.status(500).json({
      error: err.message || err.toString(),
    });
  } finally {
    if (filePath && fs.existsSync(filePath)) {
      try {
        fs.unlinkSync(filePath);
      } catch {}
    }
  }
};

export const analyzeVideo = async (req, res) => {
  let filePath;

  try {
    if (!req.file) {
      return res.status(400).json({
        error: "No video uploaded. Use form-data key: video",
      });
    }

    filePath = req.file.path;

    const result = await runPython(PYTHON_PATH, [
      PYTHON_MAIN,
      filePath,
      "--video",
      "--json",
    ]);

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
      data: json,
    });
  } catch (err) {
    return res.status(500).json({
      error: err.message || err.toString(),
    });
  } finally {
    if (filePath && fs.existsSync(filePath)) {
      try {
        fs.unlinkSync(filePath);
      } catch {}
    }
  }
};