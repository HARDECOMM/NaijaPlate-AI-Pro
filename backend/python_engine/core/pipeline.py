import os
import json
import easyocr
import datetime

from .ocr_engine import perform_standard_ocr, ai_refine_ocr, preprocess_for_night
from .plate_selector import select_best_plate
from .prefix_mapper import infer_state_from_plate
from .detector import PlateDetector

# ✅ Initialize once (IMPORTANT performance fix)
reader = easyocr.Reader(['en'])
detector = PlateDetector()

# ✅ Stable base directory (fixes os.getcwd issue)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def run_pipeline(input_image, skip_ai=False, verbose=False):
    """
    Main flow: Detection (YOLO) -> Preprocess -> OCR -> AI -> Selection
    """

    # -----------------------------
    # Validate input
    # -----------------------------
    if not os.path.exists(input_image):
        return {
            "error": f"File not found: {input_image}"
        }

    is_video_frame = "frame_process_" in input_image

    if verbose and not is_video_frame:
        print(f"\n--- Processing: {input_image} ---")

    # -----------------------------
    # 1. YOLO Detection
    # -----------------------------
    if verbose:
        print("[*] Stage 1: Detecting Plate Bounding Box (YOLO)...")

    crops, annotated_img_path = detector.detect_and_crop(input_image)

    best_overall_result = None
    highest_conf_score = -1

    conf_rank = {
        "VERIFIED_STATE_MATCH": 100,
        "HIGH_CONFIDENCE_AI": 90,
        "HIGH_CONFIDENCE_STD": 80,
        "REFINED_GUESS": 50,
        "LOW_CONFIDENCE": 20,
        "NONE": 0
    }

    # -----------------------------
    # 2. Process each crop
    # -----------------------------
    for i, candidate in enumerate(crops):

        crop_path = candidate["path"]
        box = candidate["box"]

        if verbose and len(crops) > 1:
            print(f"[*] Processing Candidate {i+1}/{len(crops)}")

        # 3. Preprocess
        processed_image = preprocess_for_night(crop_path)

        # 4. Standard OCR
        if verbose:
            print("    - Running Standard OCR...")

        standard_out = perform_standard_ocr(processed_image, reader)

        # 5. AI OCR
        ai_raw = "{}"
        if not skip_ai:
            if verbose:
                print("    - Running AI Refinement...")

            ai_raw = ai_refine_ocr(crop_path)

        # 6. Selection logic
        final_plate, confidence = select_best_plate(standard_out, ai_raw)

        # 7. State mapping
        ai_state = "NONE"
        ai_slogan = "NONE"

        try:
            ai_data = json.loads(ai_raw) if ai_raw else {}
            ai_state = ai_data.get("state", "NONE").upper()
            ai_slogan = ai_data.get("slogan", "NONE").upper()
        except:
            pass

        state_info = infer_state_from_plate(final_plate, ai_state, ai_slogan)

        current_result = {
            "plate": final_plate,
            "state": state_info["state"],
            "nickname": state_info["slogan"],
            "confidence": confidence,
            "standard_raw": standard_out,
            "ai_raw": ai_raw,
            "used_night_mode": processed_image != crop_path,
            "is_cropped": box is not None,
            "bounding_box": box,
            "annotated_detection": annotated_img_path
        }

        score = conf_rank.get(confidence, 0)

        if score > highest_conf_score and final_plate != "NOT_FOUND":
            highest_conf_score = score
            best_overall_result = current_result

    # -----------------------------
    # 8. Fallback
    # -----------------------------
    if not best_overall_result:
        return {
            "plate": "NOT_FOUND",
            "state": "UNKNOWN",
            "nickname": "N/A",
            "confidence": "NONE",
            "standard_raw": "",
            "ai_raw": "{}",
            "used_night_mode": False
        }

    res = best_overall_result

    # -----------------------------
    # 9. Save output JSON
    # -----------------------------
    output_dir = os.path.join(BASE_DIR, "data", "output")
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"result_{timestamp}.json")

    try:
        with open(output_file, "w") as f:
            json.dump(res, f, indent=4)
    except:
        pass

    # -----------------------------
    # 10. OPTIONAL logs (only if verbose)
    # -----------------------------
    if verbose:
        print("\n==============================")
        print("SUCCESSFUL ANALYSIS")
        print("==============================")
        print(f"PLATE: {res['plate']}")
        print(f"STATE: {res['state']}")
        print(f"CONFIDENCE: {res['confidence']}")
        print("==============================\n")

    # IMPORTANT: return PURE JSON object only (for Node)
    return res