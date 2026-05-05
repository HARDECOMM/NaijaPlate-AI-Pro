import express from "express";
import upload from "../middleware/upload.js";
import { analyzeFile } from "../controllers/analyze/index.js";

const router = express.Router();

router.post("/analyze", (req, res, next) => {
  upload.single("file")(req, res, (err) => {
    if (err) {
      console.error("[MULTER ERROR]", err);

      return res.status(400).json({
        error: err.message || "Upload failed",
        details: "Multer failed before analysis started.",
      });
    }

    next();
  });
}, analyzeFile);

export default router;