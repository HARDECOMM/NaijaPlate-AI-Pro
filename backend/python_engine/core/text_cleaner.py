import re


LETTER_FIX = {
    "0": "O",
    "1": "I",
    "2": "Z",
    "5": "S",
    "8": "B",
}

DIGIT_FIX = {
    "O": "0",
    "Q": "0",
    "D": "0",
    "I": "1",
    "L": "1",
    "Z": "2",
    "S": "5",
    "B": "8",
    "G": "6",
}


def raw_clean(text):
    if not text:
        return ""

    return re.sub(r"[^A-Z0-9]", "", str(text).upper())


def fix_by_position(text):
    """
    Nigerian common private plate:
    LLL-DDDLL or LLLDDDLL
    Example: ABC-123DE
    """

    text = raw_clean(text)

    if len(text) < 7:
        return text

    candidate = text[:8] if len(text) >= 8 else text
    chars = list(candidate)

    # first 3 = letters
    for i in range(min(3, len(chars))):
        chars[i] = LETTER_FIX.get(chars[i], chars[i])

    # middle = digits
    for i in range(3, min(6, len(chars))):
        chars[i] = DIGIT_FIX.get(chars[i], chars[i])

    # last 2 = letters
    if len(chars) >= 8:
        for i in range(6, 8):
            chars[i] = LETTER_FIX.get(chars[i], chars[i])

    return "".join(chars)


def normalize_plate(text):
    clean = raw_clean(text)

    if not clean:
        return ""

    # Extract likely Nigerian plate from noisy OCR
    match = re.search(r"[A-Z0-9]{3}[A-Z0-9]{3,4}[A-Z0-9]{2}", clean)
    if match:
        clean = match.group(0)

    fixed = fix_by_position(clean)

    if len(fixed) >= 8:
        prefix = fixed[:3]
        middle = fixed[3:6]
        suffix = fixed[6:8]
        return f"{prefix}-{middle}{suffix}"

    return fixed


def validate_nigeria_format(plate):
    if not plate:
        return False

    plate = plate.upper().strip()

    patterns = [
        r"^[A-Z]{3}-\d{3}[A-Z]{2}$",
        r"^[A-Z]{3}\d{3}[A-Z]{2}$",
        r"^[A-Z]{3}-\d{4}[A-Z]{2}$",
        r"^[A-Z]{3}\d{4}[A-Z]{2}$",
        r"^[A-Z]{2}-?\d{3,5}[A-Z]{1,2}$",
    ]

    return any(re.match(pattern, plate) for pattern in patterns)


def plate_without_dash(plate):
    return raw_clean(plate)