import re
import json
from .constants import LGA_STATE_MAP

def is_valid_plate_candidate(text):
    """
    Checks if the text looks like a potential plate and not an error or AI sample.
    """
    if not text or len(text) > 15: 
        return False
        
    clean_text = re.sub(r'[^A-Z0-9]', '', text.upper())
    
    # CRITICAL: Block common AI prompt examples and tutorial placeholders
    blacklist = [
        "ERROR", "NOTFOUND", "LIMIT", "NONE", "API", "FAILED", "VERSION", "MODEL", "GEMINI",
        "ABC123DE", "ABC123AB", "LSR123AB", "LSR123DE", "ABC678DE", "KJA123AB",
        "XYZ456XY", "SAMPLE", "PLATE", "NUMBER", "ABC-123-DE"
    ]
    
    if clean_text in blacklist or any(word in text.upper() for word in blacklist):
        return False
        
    return len(clean_text) >= 5

def select_best_plate(standard_text, ai_text_raw):
    """
    Orchestrates selection between standard OCR and AI-refined output.
    """
    ai_number = ""
    ai_state = ""
    ai_slogan = ""
    
    # 1. Parse AI JSON safely
    try:
        if isinstance(ai_text_raw, str) and "{" in ai_text_raw:
            clean_json = ai_text_raw.strip()
            # Clean markdown code blocks
            if "```json" in clean_json: clean_json = clean_json.split("```json")[1].split("```")[0].strip()
            
            # Find JSON boundaries
            start = clean_json.find("{")
            end = clean_json.rfind("}") + 1
            if start != -1:
                ai_data = json.loads(clean_json[start:end])
                ai_number = ai_data.get("number", "").upper()
                ai_state = ai_data.get("state", "").upper()
                ai_slogan = ai_data.get("slogan", "").upper()
        else:
            ai_number = str(ai_text_raw).upper()
    except:
        ai_number = str(ai_text_raw).upper() if ai_text_raw else ""

    # 2. Cleanup helper
    def clean(text):
        return re.sub(r'[^A-Z0-9]', '', str(text).upper())

    std_clean = clean(standard_text)
    ai_clean = clean(ai_number)

    # 3. Plate pattern: 3 Letters - 3-4 Digits - 2 Letters
    # We strictly require DIGITS in the middle to avoid letter-only hallucinations
    pattern = r'([A-Z]{3})([0-9]{3,4})([A-Z]{2})'

    def extract_and_format(text):
        if not text: return None
        match = re.search(pattern, text)
        if match:
            prefix, middle, suffix = match.groups()
            return f"{prefix}-{middle}{suffix}" # Single dash format
        return None

    # 4. Selection logic
    ai_plate = extract_and_format(ai_clean)
    if ai_plate and is_valid_plate_candidate(ai_plate):
        prefix = ai_plate.split('-')[0]
        mapped_state = LGA_STATE_MAP.get(prefix)
        confidence = "HIGH_CONFIDENCE_AI"
        if ai_state and mapped_state and ai_state in mapped_state:
            confidence = "VERIFIED_STATE_MATCH"
        return ai_plate, confidence

    std_plate = extract_and_format(std_clean)
    if std_plate and is_valid_plate_candidate(std_plate):
        return std_plate, "HIGH_CONFIDENCE_STD"

    # Fallback to raw text if it looks semi-valid
    if is_valid_plate_candidate(ai_clean) and len(ai_clean) >= 7:
        return ai_clean, "REFINED_GUESS"
    
    if is_valid_plate_candidate(std_clean) and len(std_clean) >= 6:
        return std_clean, "LOW_CONFIDENCE"

    return "NOT_FOUND", "NONE"