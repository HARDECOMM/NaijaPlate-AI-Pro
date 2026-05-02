import cv2
import os
import numpy as np
from ultralytics import YOLO

class PlateDetector:
    def __init__(self, model_path=None):
        """
        Initialize detector with a guaranteed correct model path.
        """

        # ✅ Get project root (go up from python_engine/)
        self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        # ✅ Define correct model path
        self.MODEL_PATH = os.path.join(self.BASE_DIR, "models", "best.pt")

        if os.path.exists(self.MODEL_PATH):
            print(f"[*] SUCCESS: Using custom trained weights: {self.MODEL_PATH}")
        else:
            print(f"[!] ERROR: Model not found at {self.MODEL_PATH}")
            self.model = None
            return

        try:
            self.model = YOLO(self.MODEL_PATH)
            print(f"[*] Plate Detector initialized successfully")
        except Exception as e:
            print(f"[!] Failed to load YOLO model: {e}")
            self.model = None

    def detect_and_crop(self, image_path):
        """
        Detects plates, crops them, saves annotated full image,
        and returns crops + annotated path.
        """

        # ✅ Use stable base directory (NOT os.getcwd())
        data_out = os.path.join(self.BASE_DIR, 'data', 'output')
        crops_dir = os.path.join(data_out, 'crops')
        detect_dir = os.path.join(data_out, 'detections')

        os.makedirs(crops_dir, exist_ok=True)
        os.makedirs(detect_dir, exist_ok=True)

        # Extract filename
        base_name = os.path.splitext(os.path.basename(image_path))[0]

        if self.model is None:
            return [{"path": image_path, "box": None}], None

        results = self.model.predict(image_path, conf=0.25, verbose=False)

        img = cv2.imread(image_path)
        if img is None:
            return [{"path": image_path, "box": None}], None

        img_annotated = img.copy()
        crops = []

        h, w, _ = img.shape

        for i, r in enumerate(results):
            boxes = r.boxes.xyxy.cpu().numpy()

            for j, box in enumerate(boxes):
                x1, y1, x2, y2 = map(int, box)

                # Draw bounding box
                cv2.rectangle(img_annotated, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.putText(
                    img_annotated,
                    "PLATE",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2
                )

                # Add margin (5%)
                mh = int((y2 - y1) * 0.05)
                mw = int((x2 - x1) * 0.05)

                y1_final = max(0, y1 - mh)
                y2_final = min(h, y2 + mh)
                x1_final = max(0, x1 - mw)
                x2_final = min(w, x2 + mw)

                crop = img[y1_final:y2_final, x1_final:x2_final]

                # Save crop
                crop_name = f"{base_name}_plate_{i}_{j}.jpg"
                crop_path = os.path.join(crops_dir, crop_name)
                cv2.imwrite(crop_path, crop)

                crops.append({
                    "path": crop_path,
                    "box": [x1, y1, x2, y2]
                })

        # Save annotated image
        detect_name = f"{base_name}_detected.jpg"
        detect_path = os.path.join(detect_dir, detect_name)
        cv2.imwrite(detect_path, img_annotated)

        # Fallback if no detections
        if not crops:
            print("[*] No plates detected by YOLO. Falling back to full image.")
            return [{"path": image_path, "box": None}], detect_path

        print(f"[*] YOLO detected {len(crops)} plate candidate(s). Bounding box image saved.")
        return crops, detect_path