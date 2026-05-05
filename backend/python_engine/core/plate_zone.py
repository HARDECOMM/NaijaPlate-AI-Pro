import cv2
import os

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
        3
    )

    output_path = input_path.replace(".jpg", "_processed.jpg")
    cv2.imwrite(output_path, thresh)

    return output_path