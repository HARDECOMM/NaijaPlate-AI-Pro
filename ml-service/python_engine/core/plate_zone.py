import cv2
import os

from python_engine.config.paths import PATHS


def preprocess_for_main_number(input_path):
    img = cv2.imread(input_path)

    if img is None:
        return input_path

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        15,
        3,
    )

    os.makedirs(PATHS["PREPROCESSED"], exist_ok=True)

    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)

    output_path = os.path.join(
        PATHS["PREPROCESSED"],
        f"{name}_processed{ext or '.jpg'}"
    )

    cv2.imwrite(output_path, thresh)

    return output_path