import sys
import json
import os
import contextlib

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No file provided"}))
        return

    image_path = sys.argv[1]

    try:
        # Redirect all pipeline logs away from stdout
        with contextlib.redirect_stdout(sys.stderr):
            from python_engine.core.pipeline import run_pipeline

            result = run_pipeline(
                input_image=image_path,
                skip_ai=False,
                verbose=False
            )

        if "annotated_detection" in result:
            result["annotated_detection_url"] = result.get("annotated_detection")

        # Only this goes to Node stdout
        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({
            "error": str(e),
            "plate": "ERROR",
            "state": "UNKNOWN",
            "nickname": "N/A",
            "confidence": "NONE",
            "standard_raw": "",
            "ai_raw": "{}",
            "annotated_detection_url": None
        }))


if __name__ == "__main__":
    main()