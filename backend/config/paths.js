import path from "path";

export const ROOT = process.cwd();

export const UPLOAD_DIR = path.join(
  ROOT,
  "data",
  "uploads"
);

export const OUTPUT_DIR = path.join(
  ROOT,
  "data",
  "output"
);