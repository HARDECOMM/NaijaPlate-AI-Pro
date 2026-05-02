import re


def normalize_plate(text):
    """
    Cleans and normalizes OCR plate output.
    """

    if not text:
        return ""

    clean = re.sub(r'[^A-Z0-9]', '', str(text).upper())

    # --------------------------
    # Basic OCR correction layer
    # (safe directional fixes only)
    # --------------------------
    clean = clean.replace('O', '0')  # optional (handled later carefully)
    clean = clean.replace('I', '1')

    # Restore likely letter positions for prefix (first 3 chars)
    prefix = clean[:3].replace('0', 'O').replace('1', 'I')

    middle = clean[3:-2] if len(clean) > 5 else clean[3:]
    suffix = clean[-2:] if len(clean) >= 2 else ""

    # More conservative numeric fix (avoid overcorrection)
    middle = middle.replace('O', '0').replace('S', '5')

    return f"{prefix}-{middle}{suffix}" if middle else prefix


# --------------------------
# Flexible validation
# --------------------------
def validate_nigeria_format(plate):
    """
    Validates multiple Nigerian plate formats (robust version).
    """

    if not plate:
        return False

    plate = plate.upper()

    patterns = [
        r'^[A-Z]{3}-\d{3,4}[A-Z]{2}$',   # ABC-123XY
        r'^[A-Z]{2}-\d{3,4}-[A-Z]{2}$',  # AB-123-XY
        r'^[A-Z]{3}\d{3,4}[A-Z]{2}$',    # ABC123XY
        r'^[A-Z]{2}\d{3,5}[A-Z]{1,2}$'   # Government plates
    ]

    return any(re.match(p, plate) for p in patterns)