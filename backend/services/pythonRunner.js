import { spawn } from "child_process";
import path from "path";
import { PATHS } from "../config/paths.js";

export function runPython(imagePath) {
  return new Promise((resolve, reject) => {
    const script = path.join(PATHS.PYTHON, "main.py");

    const py = spawn("python", [script, imagePath, "--json"]);

    let output = "";
    let error = "";

    py.stdout.on("data", (data) => {
      output += data.toString();
    });

    py.stderr.on("data", (data) => {
      error += data.toString();
    });

    py.on("close", (code) => {
      if (code !== 0) return reject(error);

      try {
        resolve(JSON.parse(output));
      } catch (e) {
        reject("Invalid JSON from Python");
      }
    });
  });
}