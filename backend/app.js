import express from "express";
import cors from "cors";
import routes from "./routes/routes.js";

const app = express();

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.json({
    status: "ok",
    service: "NaijaPlate Backend API",
    message: "Backend is running",
  });
});

app.get("/api/health", (req, res) => {
  res.json({
    status: "healthy",
    service: "NaijaPlate Backend API",
  });
});

app.use("/api", routes);

export default app;