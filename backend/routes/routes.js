import express from "express";
import upload from "../middleware/upload.js";

import {
  analyzeFile,
  analyzeFileRefined,
} from "../controllers/controller.js";

const router = express.Router();

router.post(
  "/analyze",
  upload.single("file"),
  analyzeFile
);

router.post(
  "/analyze-refined",
  upload.single("file"),
  analyzeFileRefined
);

export default router;