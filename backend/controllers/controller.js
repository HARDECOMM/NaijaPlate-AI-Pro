import fs from "fs";
import { analyzeWithML } from "../services/ml.service.js";

export const analyzeFile = async (req, res) => {
  let filePath;

  try {
    if (!req.file) {
      return res.status(400).json({
        error: "No file uploaded",
      });
    }

    filePath = req.file.path;

    const result = await analyzeWithML(
      filePath,
      false
    );

    return res.json(result);

  } catch (err) {
    console.error("[ANALYZE ERROR]", err);

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

export const analyzeFileRefined = async (req, res) => {
  let filePath;

  try {
    if (!req.file) {
      return res.status(400).json({
        error: "No file uploaded",
      });
    }

    filePath = req.file.path;

    const result = await analyzeWithML(
      filePath,
      true
    );

    return res.json(result);

  } catch (err) {
    console.error("[REFINED ERROR]", err);

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