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

    import argparse

    parser = argparse.ArgumentParser(description="NaijaPlate analyzer")
    parser.add_argument("path", help="Path to image or video file")
    parser.add_argument("--json", action="store_true", help="Output JSON result")
    parser.add_argument("--video", action="store_true", help="Process a video file")
    parser.add_argument("--sample-rate", type=int, default=15, help="Sample every N frames when processing video")
    parser.add_argument("--start-frame", type=int, default=35, help="Start frame offset for video processing")
    parser.add_argument("--max-frames", type=int, default=None, help="Maximum number of sampled frames for video processing")

    args = parser.parse_args()
    file_path = args.path

    try:
        # Redirect all pipeline logs away from stdout
        with contextlib.redirect_stdout(sys.stderr):
            if args.video:
                from python_engine.core.video_pipeline import process_video

                result = process_video(
                    video_path=file_path,
                    sample_rate=args.sample_rate,
                    start_frame=args.start_frame,
                    max_frames=args.max_frames,
                )
            else:
                from python_engine.core.pipeline import run_pipeline

                result = run_pipeline(
                    input_image=file_path,
                    skip_ai=False,
                    verbose=False
                )

        if "annotated_detection" in result:
            result["annotated_detection_url"] = result.get("annotated_detection")

        if "crop_path" in result:
            result["crop_url"] = result.get("crop_path")

        if "processed_path" in result:
            result["processed_url"] = result.get("processed_path")

        if "result_path" in result:
            result["result_url"] = result.get("result_path")

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