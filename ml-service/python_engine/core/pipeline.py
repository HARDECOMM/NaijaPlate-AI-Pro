import os
import json
import datetime

from python_engine.config.paths import PATHS, create_dirs
from .ocr_engine import load_ocr, perform_standard_ocr, ai_refine_ocr, preprocess_for_night
from .plate_selector import select_best_plate
from .prefix_mapper import infer_state_from_plate
from .detector import PlateDetector
from .text_cleaner import normalize_plate, validate_nigeria_format


# Initialize once
reader = load_ocr()
detector = PlateDetector()


def run_pipeline(input_image, skip_ai=False, verbose=False):
    create_dirs()

    if not os.path.exists(input_image):
        return {
            "error": f"File not found: {input_image}",
            "plate": "ERROR",
            "state": "UNKNOWN",
            "nickname": "N/A",
            "confidence": "NONE",
        }

    if verbose:
        print(f"\n--- Processing: {input_image} ---")

    crops, annotated_img_path = detector.detect_and_crop(input_image)

    if not crops:
        return {
            "plate": "NOT_FOUND",
            "state": "UNKNOWN",
            "nickname": "N/A",
            "confidence": "NONE",
            "standard_raw": "",
            "standard_cleaned": "",
            "ai_raw": "{}",
            "used_night_mode": False,
            "is_cropped": False,
            "annotated_detection": annotated_img_path,
        }

    best_result = None
    best_score = -1

    conf_rank = {
        "VERIFIED_STATE_MATCH": 100,
        "HIGH_CONFIDENCE_AI": 90,
        "HIGH_CONFIDENCE_STD": 80,
        "REFINED_GUESS": 50,
        "LOW_CONFIDENCE": 20,
        "NONE": 0,
    }

    for candidate in crops:
        crop_path = candidate.get("path")

        if not crop_path or not os.path.exists(crop_path):
            continue

        processed_path = preprocess_for_night(crop_path)

        # ✅ OCR fallback: try original crop first, then processed crop
        standard_raw = perform_standard_ocr(crop_path, reader)

        if not standard_raw:
            standard_raw = perform_standard_ocr(processed_path, reader)

        standard_cleaned = normalize_plate(standard_raw)

        ai_raw = "{}"

        if not skip_ai:
            ai_raw = ai_refine_ocr(crop_path)

            try:
                ai_json = json.loads(ai_raw)
                ai_json["number"] = normalize_plate(ai_json.get("number", ""))
                ai_raw = json.dumps(ai_json)
            except Exception:
                pass

        final_plate, confidence = select_best_plate(standard_cleaned, ai_raw)
        final_plate = normalize_plate(final_plate)

        if not validate_nigeria_format(final_plate):
            confidence = "LOW_CONFIDENCE"
            final_plate = "NOT_FOUND"

        try:
            ai_data = json.loads(ai_raw) if ai_raw else {}
        except Exception:
            ai_data = {}

        state_info = infer_state_from_plate(
            final_plate,
            ai_data.get("state", "NONE"),
            ai_data.get("slogan", "NONE"),
        )

        result = {
            "plate": final_plate,
            "state": state_info.get("state", "UNKNOWN"),
            "nickname": state_info.get("slogan", "N/A"),
            "confidence": confidence,
            "standard_raw": standard_raw,
            "standard_cleaned": standard_cleaned,
            "ai_raw": ai_raw,
            "used_night_mode": processed_path != crop_path,
            "is_cropped": True,
            "crop_path": crop_path,
            "processed_path": processed_path,
            "bounding_box": candidate.get("box"),
            "annotated_detection": annotated_img_path,
            "state_decision_source": state_info.get("decision_source", "unknown"),
            "prefix": state_info.get("prefix", ""),
            "prefix_state": state_info.get("prefix_state", "UNKNOWN"),
            "ai_state": state_info.get("ai_state", "UNKNOWN"),
            "slogan_state": state_info.get("slogan_state", "UNKNOWN"),
        }

        score = conf_rank.get(confidence, 0)

        if score > best_score and final_plate != "NOT_FOUND":
            best_score = score
            best_result = result

    if not best_result:
        best_result = {
            "plate": "NOT_FOUND",
            "state": "UNKNOWN",
            "nickname": "N/A",
            "confidence": "NONE",
            "standard_raw": "",
            "standard_cleaned": "",
            "ai_raw": "{}",
            "used_night_mode": False,
            "is_cropped": False,
            "annotated_detection": annotated_img_path,
        }

    result_filename = f"result_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    result_path = os.path.join(PATHS["RESULTS"], result_filename)

    try:
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(best_result, f, indent=4)
    except Exception as e:
        best_result["save_error"] = str(e)

    best_result["result_path"] = result_path

    return best_result