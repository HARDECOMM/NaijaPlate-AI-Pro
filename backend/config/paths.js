// import path from "path";

// export const ROOT = process.cwd();

// export const UPLOAD_DIR = path.join(ROOT, "data", "uploads");
// export const OUTPUT_DIR = path.join(ROOT, "data", "output");

// export const PYTHON_PATH =
//   process.env.PYTHON_PATH ||
//   (process.platform === "win32"
//     ? path.join(ROOT, "python_engine", "venv", "Scripts", "python.exe")
//     : "python3");

// export const PYTHON_MAIN = path.join(ROOT, "python_engine", "main.py");


// production
import path from "path";

export const ROOT = process.cwd();

export const UPLOAD_DIR = path.join(ROOT, "data", "uploads");
export const OUTPUT_DIR = path.join(ROOT, "data", "output");

export const PYTHON_PATH = process.env.PYTHON_PATH || "python";

export const PYTHON_MAIN = path.join(ROOT, "python_engine", "main.py");