import cv2
import numpy as np


def preprocess_for_main_number(input_path, output_path):
    """
    Preprocess image for OCR (optimized for license plates).
    """

    img = cv2.imread(input_path)

    if img is None:
        print(f"[!] Preprocess failed: image not found -> {input_path}")
        return False

    # -------------------------
    # 1. Resize (controlled upscale)
    # -------------------------
    height, width = img.shape[:2]

    # safer scaling (avoid over-blur)
    scale = 2.0 if max(height, width) < 1000 else 1.5

    img = cv2.resize(
        img,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC
    )

    # -------------------------
    # 2. Grayscale
    # -------------------------
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # -------------------------
    # 3. Light denoise (IMPORTANT improvement)
    # -------------------------
    gray = cv2.fastNlMeansDenoising(gray, None, 25, 7, 21)

    # -------------------------
    # 4. Contrast enhancement (CLAHE)
    # -------------------------
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # -------------------------
    # 5. Mild blur (reduce noise before OCR)
    # -------------------------
    blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)

    # -------------------------
    # 6. Adaptive threshold (kept but softened)
    # -------------------------
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        15,
        4
    )

    # -------------------------
    # 7. Save output
    # -------------------------
    cv2.imwrite(output_path, thresh)

    return True