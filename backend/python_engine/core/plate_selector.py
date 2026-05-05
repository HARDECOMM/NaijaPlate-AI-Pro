import re
import json

from .text_cleaner import normalize_plate, validate_nigeria_format, raw_clean
from .constants import LGA_STATE_MAP


BLACKLIST = {
    "ERROR", "NOTFOUND", "LIMIT", "NONE", "API", "FAILED", "VERSION",
    "MODEL", "GEMINI", "SAMPLE", "PLATE", "NUMBER", "ABC123DE",
    "ABC123AB", "XYZ456XY", "KJA123AB",
}


def is_valid_plate_candidate(text):
    if not text:
        return False

    clean = raw_clean(text)

    if len(clean) < 6 or len(clean) > 10:
        return False

    if clean in BLACKLIST:
        return False

    if any(word in clean for word in BLACKLIST):
        return False

    return True


def parse_ai_json(ai_text_raw):
    if not ai_text_raw:
        return {}

    try:
        text = str(ai_text_raw).strip()

        if "```" in text:
            text = text.replace("```json", "").replace("```", "").strip()

        start = text.find("{")
        end = text.rfind("}") + 1

        if start != -1 and end > start:
            return json.loads(text[start:end])

    except Exception:
        pass

    return {}


def select_best_plate(standard_text, ai_text_raw):
    ai_data = parse_ai_json(ai_text_raw)

    ai_number = ai_data.get("number", "")
    ai_state = str(ai_data.get("state", "")).upper()
    ai_slogan = str(ai_data.get("slogan", "")).upper()

    std_plate = normalize_plate(standard_text)
    ai_plate = normalize_plate(ai_number)

    # 1. Prefer Gemini if it gives valid Nigerian format
    if validate_nigeria_format(ai_plate) and is_valid_plate_candidate(ai_plate):
        prefix = raw_clean(ai_plate)[:3]
        mapped_state = LGA_STATE_MAP.get(prefix, "")

        if ai_state and mapped_state and ai_state in mapped_state:
            return ai_plate, "VERIFIED_STATE_MATCH"

        if ai_slogan:
            return ai_plate, "HIGH_CONFIDENCE_AI"

        return ai_plate, "HIGH_CONFIDENCE_AI"

    # 2. Use standard OCR if valid
    if validate_nigeria_format(std_plate) and is_valid_plate_candidate(std_plate):
        return std_plate, "HIGH_CONFIDENCE_STD"

    # 3. Gemini fallback
    if is_valid_plate_candidate(ai_plate):
        return ai_plate, "REFINED_GUESS"

    # 4. OCR fallback
    if is_valid_plate_candidate(std_plate):
        return std_plate, "LOW_CONFIDENCE"

    return "NOT_FOUND", "NONE"