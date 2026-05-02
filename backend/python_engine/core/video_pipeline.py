import cv2
import os
import json
import datetime
from collections import defaultdict
from .pipeline import run_pipeline


def process_video(video_path, sample_rate=15, start_frame=35):

    if not os.path.exists(video_path):
        print(f"Error: Video not found -> {video_path}")
        return

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Cannot open video")
        return

    if start_frame:
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    print(f"[*] Video loaded | Frames: {total_frames} | FPS: {fps}")

    tracking_history = {}
    frame_count = start_frame

    data_out = os.path.join(os.getcwd(), "data", "output")
    best_dir = os.path.join(data_out, "best_video_frames")
    os.makedirs(best_dir, exist_ok=True)

    # -----------------------------
    # FRAME LOOP
    # -----------------------------
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % sample_rate == 0:

            print(f"\rProcessing frame {frame_count}/{total_frames}", end="")

            try:
                # -------------------------
                # Run pipeline (MEMORY SAFE MODE)
                # -------------------------
                result = run_pipeline_from_frame(frame, skip_ai=True)

                plate = result.get("plate")

                if not plate or plate == "NOT_FOUND":
                    frame_count += 1
                    continue

                # -------------------------
                # INIT TRACK
                # -------------------------
                if plate not in tracking_history:
                    tracking_history[plate] = {
                        "hits": 0,
                        "states": defaultdict(int),
                        "best_frame": None,
                        "best_score": -1
                    }

                stats = tracking_history[plate]
                stats["hits"] += 1

                state = result.get("state", "UNKNOWN")
                stats["states"][state] += 1

                # -------------------------
                # IMPROVED SCORING
                # -------------------------
                conf = result.get("confidence", "NONE")

                score_map = {
                    "VERIFIED_STATE_MATCH": 100,
                    "HIGH_CONFIDENCE_AI": 90,
                    "HIGH_CONFIDENCE_STD": 80,
                    "REFINED_GUESS": 50,
                    "LOW_CONFIDENCE": 20
                }

                score = score_map.get(conf, 0) + stats["hits"]  # temporal boost

                if score > stats["best_score"]:
                    stats["best_score"] = score
                    stats["best_frame"] = frame.copy()  # MEMORY storage (no disk)

            except:
                pass

        frame_count += 1

    cap.release()
    print("\n")

    # -----------------------------
    # FINAL AI REFINEMENT
    # -----------------------------
    final_results = {}

    print(f"[*] Refining {len(tracking_history)} plates...")

    for plate, stats in tracking_history.items():

        if stats["best_frame"] is None:
            continue

        majority_state = max(stats["states"], key=stats["states"].get)

        # Save best frame ONCE
        filename = f"{plate.replace('-','_')}_{datetime.datetime.now().timestamp()}.jpg"
        save_path = os.path.join(best_dir, filename)

        cv2.imwrite(save_path, stats["best_frame"])

        # Run full pipeline once
        refined = run_pipeline(save_path, skip_ai=False)

        # State correction logic
        if refined["state"] == "UNKNOWN STATE":
            refined["state"] = majority_state

        refined["video_hits"] = stats["hits"]
        final_results[plate] = refined

    # -----------------------------
    # SUMMARY
    # -----------------------------
    print("\n==============================")
    print("VIDEO SUMMARY")
    print("==============================")

    for plate, res in final_results.items():
        print(f"{plate} | {res['state']} | hits: {res['video_hits']}")

    print("==============================\n")

    # -----------------------------
    # SAVE OUTPUT
    # -----------------------------
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    summary_file = os.path.join(data_out, f"video_summary_{ts}.json")

    with open(summary_file, "w") as f:
        json.dump(final_results, f, indent=4)

    print(f"Saved: {summary_file}")

    return final_results


# -----------------------------
# MEMORY-BASED PIPELINE WRAPPER
# -----------------------------
def run_pipeline_from_frame(frame, skip_ai=True):
    """
    Avoids disk I/O by feeding frame directly.
    """

    temp_path = os.path.join(os.getcwd(), "temp_frame.jpg")
    cv2.imwrite(temp_path, frame)

    result = run_pipeline(temp_path, skip_ai=skip_ai)

    if os.path.exists(temp_path):
        os.remove(temp_path)

    return result