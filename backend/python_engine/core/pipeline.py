import os
import json
import datetime

from .ocr_engine import perform_standard_ocr, ai_refine_ocr, preprocess_for_night
from .plate_selector import select_best_plate
from .prefix_mapper import infer_state_from_plate
from .detector import PlateDetector
from .text_cleaner import normalize_plate, validate_nigeria_format  # 👈 ADD THIS

# Init once
reader = None  # (keep your existing EasyOCR init outside if already global)
detector = PlateDetector()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def run_pipeline(input_image, skip_ai=False, verbose=False):

    if not os.path.exists(input_image):
        return {"error": f"File not found: {input_image}"}

    if verbose:
        print(f"\n--- Processing: {input_image} ---")

    # -----------------------------
    # YOLO DETECTION
    # -----------------------------
    if verbose:
        print("[*] YOLO detection stage...")

    crops, annotated_img_path = detector.detect_and_crop(input_image)

    best_result = None
    best_score = -1

    conf_rank = {
        "VERIFIED_STATE_MATCH": 100,
        "HIGH_CONFIDENCE_AI": 90,
        "HIGH_CONFIDENCE_STD": 80,
        "REFINED_GUESS": 50,
        "LOW_CONFIDENCE": 20,
        "NONE": 0
    }

    # -----------------------------
    # PROCESS EACH CROP
    # -----------------------------
    for candidate in crops:

        crop_path = candidate["path"]

        # 1. preprocess
        processed = preprocess_for_night(crop_path)

        # 2. OCR
        standard_out = perform_standard_ocr(processed, reader)
        standard_out = normalize_plate(standard_out)  # 🔥 FIX HERE

        # 3. AI OCR (optional)
        ai_raw = "{}"
        if not skip_ai:
            ai_raw = ai_refine_ocr(crop_path)

            # normalize AI output
            try:
                ai_json = json.loads(ai_raw)
                ai_json["number"] = normalize_plate(ai_json.get("number", ""))
                ai_raw = json.dumps(ai_json)
            except:
                pass

        # 4. select best plate
        final_plate, confidence = select_best_plate(standard_out, ai_raw)

        # 🔥 FINAL VALIDATION (CRITICAL FIX)
        if not validate_nigeria_format(final_plate):
            confidence = "LOW_CONFIDENCE"
            final_plate = "NOT_FOUND"

        # 5. state inference
        try:
            ai_data = json.loads(ai_raw) if ai_raw else {}
        except:
            ai_data = {}

        state_info = infer_state_from_plate(
            final_plate,
            ai_data.get("state", "NONE"),
            ai_data.get("slogan", "NONE")
        )

        result = {
            "plate": final_plate,
            "state": state_info["state"],
            "nickname": state_info["slogan"],
            "confidence": confidence,
            "standard_raw": standard_out,
            "ai_raw": ai_raw,
            "annotated_detection": annotated_img_path
        }

        score = conf_rank.get(confidence, 0)

        if score > best_score and final_plate != "NOT_FOUND":
            best_score = score
            best_result = result

    # -----------------------------
    # FALLBACK
    # -----------------------------
    if not best_result:
        return {
            "plate": "NOT_FOUND",
            "state": "UNKNOWN",
            "nickname": "N/A",
            "confidence": "NONE"
        }

    # -----------------------------
    # SAVE OUTPUT
    # -----------------------------
    out_dir = os.path.join(BASE_DIR, "data", "output")
    os.makedirs(out_dir, exist_ok=True)

    file_path = os.path.join(out_dir, f"result_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    try:
        with open(file_path, "w") as f:
            json.dump(best_result, f, indent=4)
    except:
        pass

    return best_result