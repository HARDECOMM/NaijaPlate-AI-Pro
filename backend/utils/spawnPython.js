import { spawn } from "child_process";

export function runPython(command, args = []) {
  return new Promise((resolve, reject) => {
    const py = spawn(command, args);

    let stdout = "";
    let stderr = "";

    py.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    py.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    py.on("close", (code) => {
      console.log("[PYTHON EXIT CODE]", code);

      if (stderr) {
        console.error("[PYTHON STDERR]", stderr);
      }

      if (code !== 0) {
        return reject(stderr || "Python failed");
      }

      resolve(stdout);
    });

    py.on("error", (err) => {
      reject("Spawn error: " + err.message);
    });
  });
}