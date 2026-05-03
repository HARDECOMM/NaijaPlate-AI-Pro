import express from "express";
import multer from "multer";
import fs from "fs";
import cors from "cors";
import path from "path";

import { PYTHON_PATH, PYTHON_MAIN, UPLOAD_DIR, OUTPUT_DIR } from "./config/paths.js";
import { runPython } from "./utils/spawnPython.js";

const app = express();
const PORT = process.env.PORT || 5000;

// ✅ CREATE REQUIRED DIRECTORIES (important for Render)
fs.mkdirSync(UPLOAD_DIR, { recursive: true });
fs.mkdirSync(OUTPUT_DIR, { recursive: true });

// ✅ ENV-BASED CORS (PRODUCTION READY)
const allowedOrigins = process.env.FRONTEND_URLS
  ? process.env.FRONTEND_URLS.split(",").map((url) => url.trim())
  : ["http://localhost:5173", "http://127.0.0.1:5173"];

app.use(
  cors({
    origin: (origin, callback) => {
      // Allow Postman / server requests (no origin)
      if (!origin) return callback(null, true);

      if (allowedOrigins.includes(origin)) {
        return callback(null, true);
      }

      return callback(new Error(`CORS blocked: ${origin}`));
    },
  })
);

app.use(express.json());

// ✅ MULTER STORAGE CONFIG
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

// ✅ ROOT ROUTE
app.get("/", (req, res) => {
  res.send("🚀 PlateSight AI Backend Running");
});

// ✅ HEALTH CHECK (DEBUGGING)
app.get("/api/health", (req, res) => {
  res.json({
    status: "ok",
    pythonPath: PYTHON_PATH,
    pythonMain: PYTHON_MAIN,
  });
});

// ✅ MAIN ANALYZE ROUTE
app.post("/api/analyze", upload.single("image"), async (req, res) => {
  let filePath;

  try {
    if (!req.file) {
      return res.status(400).json({
        error: "No image uploaded. Use form-data key: image",
      });
    }

    filePath = req.file.path;

    console.log("[API] Image received:", filePath);

    // ✅ Check Python script exists
    if (!fs.existsSync(PYTHON_MAIN)) {
      return res.status(500).json({
        error: "Python main.py not found",
        path: PYTHON_MAIN,
      });
    }

    // ✅ Run Python
    const result = await runPython(PYTHON_PATH, [
      PYTHON_MAIN,
      filePath,
      "--json",
    ]);

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
      data: json,
    });

  } catch (err) {
    console.error("[SERVER ERROR]", err);

    return res.status(500).json({
      error: err.message || err.toString(),
    });

  } finally {
    // ✅ Clean uploaded file
    if (filePath && fs.existsSync(filePath)) {
      try {
        fs.unlinkSync(filePath);
      } catch {}
    }
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});