import express from "express";
import multer from "multer";
import fs from "fs";
import cors from "cors";
import path from "path"; // ✅ ADD THIS

import { PYTHON_PATH, PYTHON_MAIN, UPLOAD_DIR } from "./config/paths.js";
import { runPython } from "./utils/spawnPython.js";

const app = express();
const PORT = process.env.PORT || 5000;

// ✅ FIX: store file WITH extension
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, UPLOAD_DIR);
  },
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname) || ".jpg";
    const filename = `${Date.now()}-${Math.round(Math.random() * 1e9)}${ext}`;
    cb(null, filename);
  },
});

const upload = multer({ storage });

// ✅ CORS
app.use(cors({
  origin: ["http://localhost:5173", "http://127.0.0.1:5173"],
}));

app.use(express.json());

// ✅ ROOT ROUTE
app.get("/", (req, res) => {
  res.send("🚀 PlateSight AI Backend Running");
});

app.post("/api/analyze", upload.single("image"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No image uploaded" });
    }

    const filePath = req.file.path;

    console.log("[API] Image received:", filePath);

    // ✅ CHECK PYTHON FILE EXISTS
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

    console.log("[PYTHON RAW OUTPUT]");
    console.log(result);

    let json;
    try {
      json = JSON.parse(result);
    } catch (err) {
      return res.status(500).json({
        error: "Invalid JSON from Python",
        raw: result,
      });
    }

    // ✅ DELETE FILE SAFELY
    try {
      fs.unlinkSync(filePath);
    } catch {}

    return res.json({
      status: "success",
      data: json,
    });

  } catch (err) {
    console.error("[SERVER ERROR]", err);

    return res.status(500).json({
      error: err.toString(),
    });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});