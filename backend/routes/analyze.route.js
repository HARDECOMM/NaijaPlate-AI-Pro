import express from "express";
import upload from "../middleware/upload.js";
import { analyzeImage } from "../controllers/analyze.controller.js";

const router = express.Router();

router.post("/analyze", upload.single("image"), analyzeImage);

export default router;