import cv2
import os
import json
import datetime
from collections import defaultdict

from python_engine.config.paths import PATHS, create_dirs
from .pipeline import run_pipeline
from .video_tracker import VehicleTracker


def process_video(video_path, sample_rate=15, start_frame=35, max_frames=None):
    """
    Video prototype pipeline:
    1. Samples frames from video
    2. Runs fast OCR pipeline without Gemini
    3. Groups repeated plate readings
    4. Saves best frames
    5. Runs full Gemini refinement once per final candidate
    """

    create_dirs()

    if not os.path.exists(video_path):
        return {
            "error": f"Video not found: {video_path}",
            "results": {}
        }

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return {
            "error": "Cannot open video",
            "results": {}
        }

    if start_frame:
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    print(f"[*] Video loaded | Frames: {total_frames} | FPS: {fps}")

    best_dir = os.path.join(PATHS["OUTPUT"], "best_video_frames")
    temp_dir = os.path.join(PATHS["OUTPUT"], "temp_video_frames")
    video_results_dir = os.path.join(PATHS["RESULTS"], "video")

    os.makedirs(best_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(video_results_dir, exist_ok=True)

    tracker = VehicleTracker(iou_threshold=0.35, max_missed=7)
    frame_count = start_frame
    processed_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if max_frames is not None and processed_count >= max_frames:
            break

        if frame_count % sample_rate == 0:
            print(f"\rProcessing frame {frame_count}/{total_frames}", end="")

            temp_path = os.path.join(
                temp_dir,
                f"frame_{frame_count}_{datetime.datetime.now().timestamp()}.jpg"
            )

            try:
                cv2.imwrite(temp_path, frame)

                # Fast mode: skip Gemini while scanning many frames
                result = run_pipeline(temp_path, skip_ai=True, verbose=False)

                plate = result.get("plate", "NOT_FOUND")

                if not plate or plate == "NOT_FOUND":
                    frame_count += 1
                    processed_count += 1
                    continue

                best_frame_name = f"{plate.replace('-', '_')}_frame_{frame_count}.jpg"
                best_frame_path = os.path.join(best_dir, best_frame_name)

                tracker.update(result, frame_count, best_frame_path)
                if result.get("bounding_box") and result.get("plate") != "NOT_FOUND":
                    # Write only when a track accepts this frame as its current best
                    current_tracks = tracker.get_active_tracks()
                    if any(track.best_frame_path == best_frame_path for track in current_tracks):
                        cv2.imwrite(best_frame_path, frame)

            except Exception as e:
                print(f"\n[VIDEO FRAME ERROR] frame={frame_count}: {e}")

            finally:
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass

            processed_count += 1

        frame_count += 1

    cap.release()
    print("\n")

    final_results = {}
    final_tracks = tracker.get_final_tracks()

    print(f"[*] Refining {len(final_tracks)} track candidates...")

    for track in final_tracks:
        best_frame_path = track.best_frame_path

        if not best_frame_path or not os.path.exists(best_frame_path):
            continue

        majority_state = "UNKNOWN"

        if track.state_counts:
            majority_state = max(track.state_counts, key=track.state_counts.get)

        refined = run_pipeline(best_frame_path, skip_ai=False, verbose=False)

        if refined.get("state") in ["UNKNOWN", "UNKNOWN STATE", "", None]:
            refined["state"] = majority_state

        refined["video_hits"] = track.hits
        refined["best_frame_path"] = best_frame_path
        refined["video_track_id"] = track.track_id
        refined["video_candidate"] = track.plate
        refined["video_state_votes"] = dict(track.state_counts)

        final_results[f"{track.plate}_{track.track_id}"] = refined

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = os.path.join(video_results_dir, f"video_summary_{ts}.json")

    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=4)

    print("==============================")
    print("VIDEO SUMMARY")
    print("==============================")

    for track_key, res in final_results.items():
        print(f"{track_key} | {res.get('state')} | hits: {res.get('video_hits')}")

    print("==============================")
    print(f"Saved: {summary_file}")

    return {
        "summary_path": summary_file,
        "results": final_results
    }