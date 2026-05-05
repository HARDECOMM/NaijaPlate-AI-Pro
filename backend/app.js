import express from "express";
import cors from "cors";
import analyzeRoutes from "./routes/analyze.routes.js";

const app = express();

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.send("🚀 NaijaPlate AI Backend Running");
});

app.use("/api", analyzeRoutes);

// MUST BE LAST
app.use((err, req, res, next) => {
  console.error("[GLOBAL ERROR]", err);

  return res.status(500).json({
    error: err.message || "Internal Server Error",
    details: "Backend crashed before completing request.",
  });
});

export default app;