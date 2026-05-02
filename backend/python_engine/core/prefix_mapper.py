from .constants import LGA_STATE_MAP, STATE_SLOGAN_MAP
import re


def clean_text(text):
    if not text:
        return ""
    return re.sub(r'[^A-Z0-9]', '', text.upper())


def infer_state_from_plate(plate_text, ai_state="NONE", ai_slogan="NONE"):
    """
    Infer Nigerian state from plate prefix + AI hints.
    """

    # -------------------------
    # 1. Normalize plate text
    # -------------------------
    plate_clean = clean_text(plate_text)

    prefix = plate_clean[:3] if len(plate_clean) >= 3 else ""

    # -------------------------
    # 2. Prefix mapping (primary)
    # -------------------------
    state = LGA_STATE_MAP.get(prefix, "UNKNOWN STATE")

    # -------------------------
    # 3. AI state fallback (safe match)
    # -------------------------
    ai_state_clean = ai_state.upper() if ai_state else ""

    if state == "UNKNOWN STATE" and ai_state_clean:
        for known_state in STATE_SLOGAN_MAP.keys():
            if known_state == ai_state_clean:
                state = known_state
                break

    # -------------------------
    # 4. AI slogan mapping (safer matching)
    # -------------------------
    ai_slogan_clean = ai_slogan.upper() if ai_slogan else ""

    if state == "UNKNOWN STATE" and ai_slogan_clean:
        for known_state, slogan in STATE_SLOGAN_MAP.items():
            if slogan and slogan in ai_slogan_clean:
                state = known_state
                break

    # -------------------------
    # 5. Keyword fallback (STRICTER)
    # -------------------------
    if state == "UNKNOWN STATE" and ai_slogan_clean:
        slogan_keywords = {
            "SOLID MINERALS": "NASARAWA",
            "EXCELLENCE": "LAGOS",
            "PACESETTER": "OYO",
            "UNITY": "FCT ABUJA",
            "TREASURE BASE": "RIVERS",
            "LIBERAL HEART": "KADUNA",
            "BIG HEART": "DELTA",
            "LIGHT OF THE NATION": "ANAMBRA",
            "GOD'S OWN": "ABIA"
        }

        for kw, mapped_state in slogan_keywords.items():
            if kw in ai_slogan_clean:
                state = mapped_state
                break

    # -------------------------
    # 6. Final slogan resolution
    # -------------------------
    slogan = STATE_SLOGAN_MAP.get(state, "N/A")

    if (not slogan or slogan == "N/A") and ai_slogan_clean:
        slogan = ai_slogan_clean

    return {
        "state": state,
        "slogan": slogan
    }