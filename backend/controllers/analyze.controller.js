import { runPython } from "../services/pythonRunner.js";

export const analyzeImage = async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ error: "No image" });

    const result = await runPython(req.file.path);

    res.json({
      status: "success",
      data: result,
    });
  } catch (err) {
    res.status(500).json({
      status: "error",
      message: err.toString(),
    });
  }
};