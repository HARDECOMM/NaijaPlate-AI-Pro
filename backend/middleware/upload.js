import multer from "multer";
import { PATHS } from "../config/paths.js";

const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, PATHS.UPLOADS),
  filename: (req, file, cb) =>
    cb(null, `${Date.now()}_${file.originalname}`),
});

export default multer({ storage });