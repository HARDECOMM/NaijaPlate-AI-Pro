import cv2
import os
import json
import datetime

from python_engine.config.paths import PATHS, create_dirs
from .pipeline import run_pipeline
from .video_tracker import VehicleTracker


def draw_plate_box(frame, result, track_id=None):
    box = result.get("bounding_box")

    if not box or len(box) != 4:
        return frame

    x1, y1, x2, y2 = map(int, box)

    plate = result.get("plate", "UNKNOWN")
    state = result.get("state", "UNKNOWN")
    confidence = result.get("confidence", "NONE")

    label = f"ID:{track_id or '?'} | {plate} | {state}"

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

    label_y = max(y1 - 10, 30)
    label_width = min(620, frame.shape[1] - x1 - 5)

    cv2.rectangle(
        frame,
        (x1, label_y - 28),
        (x1 + label_width, label_y + 8),
        (0, 0, 0),
        -1,
    )

    cv2.putText(
        frame,
        label,
        (x1 + 5, label_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        frame,
        confidence,
        (x1 + 5, min(y2 + 30, frame.shape[0] - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2,
        cv2.LINE_AA,
    )

    return frame


def initialize_video_writer(annotated_dir, ts, fps, width, height):
    """
    Creates a reliable OpenCV video writer.

    AVI/XVID is more reliable locally.
    MP4/mp4v is used as fallback.
    """

    # First try AVI/XVID — most reliable locally
    annotated_video_path = os.path.join(
        annotated_dir,
        f"annotated_video_{ts}.avi",
    )

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    writer = cv2.VideoWriter(
        annotated_video_path,
        fourcc,
        fps,
        (width, height),
    )

    if writer.isOpened():
        print(f"[*] VideoWriter initialized: {annotated_video_path}")
        return writer, annotated_video_path

    print("[!] XVID writer failed. Trying MP4V fallback...")

    # Fallback to MP4/mp4v
    annotated_video_path = os.path.join(
        annotated_dir,
        f"annotated_video_{ts}.mp4",
    )

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(
        annotated_video_path,
        fourcc,
        fps,
        (width, height),
    )

    if writer.isOpened():
        print(f"[*] VideoWriter initialized: {annotated_video_path}")
        return writer, annotated_video_path

    raise RuntimeError("Could not initialize VideoWriter for annotated output")


def process_video(video_path, sample_rate=15, start_frame=100, max_frames=None):
    """
    Video pipeline:
    1. Reads video
    2. Samples frames
    3. Detects plates per sampled frame
    4. Tracks repeated plate detections
    5. Draws bounding boxes on video
    6. Saves annotated video
    7. Saves summary JSON
    """

    create_dirs()

    if not os.path.exists(video_path):
        return {
            "error": f"Video not found: {video_path}",
            "results": {},
        }

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return {
            "error": "Cannot open video",
            "results": {},
        }

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if width <= 0 or height <= 0:
        cap.release()
        return {
            "error": "Invalid video dimensions",
            "results": {},
        }

    if start_frame:
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    print(f"[*] Video loaded | Frames: {total_frames} | FPS: {fps}")
    print(f"[*] Video size: {width}x{height}")

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    best_dir = os.path.join(PATHS["OUTPUT"], "best_video_frames")
    temp_dir = os.path.join(PATHS["OUTPUT"], "temp_video_frames")
    annotated_dir = os.path.join(PATHS["OUTPUT"], "annotated_videos")
    video_results_dir = os.path.join(PATHS["RESULTS"], "video")

    os.makedirs(best_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(annotated_dir, exist_ok=True)
    os.makedirs(video_results_dir, exist_ok=True)

    writer, annotated_video_path = initialize_video_writer(
        annotated_dir=annotated_dir,
        ts=ts,
        fps=fps,
        width=width,
        height=height,
    )

    tracker = VehicleTracker(iou_threshold=0.35, max_missed=10)

    frame_count = start_frame
    processed_count = 0

    last_drawn_results = []

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            if max_frames is not None and processed_count >= max_frames:
                break

            annotated_frame = frame.copy()

            if frame_count % sample_rate == 0:
                print(f"\rProcessing frame {frame_count}/{total_frames}", end="")

                temp_path = os.path.join(
                    temp_dir,
                    f"frame_{frame_count}_{datetime.datetime.now().timestamp()}.jpg",
                )

                try:
                    cv2.imwrite(temp_path, frame)

                    # Fast scan mode: skip Gemini while scanning many frames
                    result = run_pipeline(temp_path, skip_ai=True, verbose=False)

                    plate = result.get("plate", "NOT_FOUND")
                    box = result.get("bounding_box")

                    if plate and plate != "NOT_FOUND" and box and len(box) == 4:
                        best_frame_name = (
                            f"{plate.replace('-', '_')}_frame_{frame_count}.jpg"
                        )
                        best_frame_path = os.path.join(best_dir, best_frame_name)

                        tracker.update(result, frame_count, best_frame_path)

                        active_tracks = tracker.get_active_tracks()
                        matched_track_id = None

                        for track in active_tracks:
                            if track.last_frame == frame_count:
                                matched_track_id = track.track_id

                                if track.best_frame_path == best_frame_path:
                                    cv2.imwrite(best_frame_path, frame)

                                break

                        result["video_track_id"] = matched_track_id
                        last_drawn_results = [result]

                except Exception as e:
                    print(f"\n[VIDEO FRAME ERROR] frame={frame_count}: {e}")

                finally:
                    if os.path.exists(temp_path):
                        try:
                            os.remove(temp_path)
                        except Exception:
                            pass

                processed_count += 1

            # Draw last known detection on non-sampled frames too
            for draw_result in last_drawn_results:
                annotated_frame = draw_plate_box(
                    annotated_frame,
                    draw_result,
                    draw_result.get("video_track_id"),
                )

            writer.write(annotated_frame)
            frame_count += 1

    finally:
        cap.release()
        writer.release()

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
        refined["video_frames_seen"] = track.last_frame - track.first_frame + 1

        final_results[f"{track.plate}_{track.track_id}"] = refined

    summary_file = os.path.join(
        video_results_dir,
        f"video_summary_{ts}.json",
    )

    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=4)

    print("==============================")
    print("VIDEO SUMMARY")
    print("==============================")

    for track_key, res in final_results.items():
        print(
            f"{track_key} | {res.get('state')} | hits: {res.get('video_hits')}"
        )

    print("==============================")
    print(f"Summary saved: {summary_file}")
    print(f"Annotated video saved: {annotated_video_path}")

    return {
        "summary_path": summary_file,
        "annotated_video_path": annotated_video_path,
        "video_format": annotated_video_path.split(".")[-1],
        "results": final_results,
    }