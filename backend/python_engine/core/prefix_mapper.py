import re

from .constants import LGA_STATE_MAP, STATE_SLOGAN_MAP, STATE_ALIASES
from .text_cleaner import raw_clean


def normalize_state_name(state):
    if not state:
        return ""

    state = str(state).upper().strip()
    state = STATE_ALIASES.get(state, state)

    return state


def clean_slogan(text):
    if not text:
        return ""

    return re.sub(r"[^A-Z0-9 ]", "", str(text).upper()).strip()


def slogan_to_state(ai_slogan):
    slogan_clean = clean_slogan(ai_slogan)

    if not slogan_clean:
        return ""

    for state, slogan in STATE_SLOGAN_MAP.items():
        if slogan and slogan.upper() in slogan_clean:
            return normalize_state_name(state)

    keyword_map = {
        "UNITY": "FCT ABUJA",
        "EXCELLENCE": "LAGOS",
        "TREASURE": "RIVERS",
        "PACESETTER": "OYO",
        "COMMERCE": "KANO",
        "BIG HEART": "DELTA",
        "LIGHT OF THE NATION": "ANAMBRA",
        "GOD": "ABIA",
        "GATEWAY": "OGUN",
        "SOLID MINERALS": "NASARAWA",
    }

    for keyword, state in keyword_map.items():
        if keyword in slogan_clean:
            return normalize_state_name(state)

    return ""


def infer_state_from_plate(plate_text, ai_state="NONE", ai_slogan="NONE"):
    """
    Safe decision logic:
    1. Use prefix if reliable.
    2. Use AI state/slogan if prefix is unknown.
    3. If prefix and AI conflict, prefer AI when slogan supports it.
    """

    plate_clean = raw_clean(plate_text)
    prefix = plate_clean[:3] if len(plate_clean) >= 3 else ""

    prefix_state = normalize_state_name(LGA_STATE_MAP.get(prefix, ""))
    ai_state_clean = normalize_state_name(ai_state if ai_state != "NONE" else "")
    slogan_state = slogan_to_state(ai_slogan if ai_slogan != "NONE" else "")

    final_state = "UNKNOWN"
    decision_source = "unknown"

    # Case 1: AI slogan is strong evidence
    if slogan_state:
        final_state = slogan_state
        decision_source = "ai_slogan"

    # Case 2: AI state is available and prefix is missing
    elif ai_state_clean and not prefix_state:
        final_state = ai_state_clean
        decision_source = "ai_state"

    # Case 3: prefix known and no AI contradiction
    elif prefix_state:
        final_state = prefix_state
        decision_source = "prefix"

    # Case 4: fallback
    elif ai_state_clean:
        final_state = ai_state_clean
        decision_source = "ai_state_fallback"

    slogan = STATE_SLOGAN_MAP.get(final_state, "N/A")

    if slogan == "N/A" and ai_slogan and ai_slogan != "NONE":
        slogan = clean_slogan(ai_slogan)

    return {
        "state": final_state,
        "slogan": slogan,
        "prefix": prefix,
        "prefix_state": prefix_state or "UNKNOWN",
        "ai_state": ai_state_clean or "UNKNOWN",
        "slogan_state": slogan_state or "UNKNOWN",
        "decision_source": decision_source,
    }