import path from "path";

export const ROOT = process.cwd();

export const UPLOAD_DIR = path.join(ROOT, "data", "uploads");
export const OUTPUT_DIR = path.join(ROOT, "data", "output");

export const PYTHON_PATH =
  "C:/Users/ademo/AppData/Local/Programs/Python/Python311/python.exe";

export const PYTHON_MAIN = path.join(ROOT, "python_engine", "main.py");