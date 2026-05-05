import cv2
import os
import torch
from ultralytics import YOLO

from python_engine.config.paths import PATHS, create_dirs


class PlateDetector:
    def __init__(self, model_path=None):
        create_dirs()

        self.MODEL_PATH = model_path or PATHS["MODEL"]
        self.device = 0 if torch.cuda.is_available() else "cpu"

        print(f"[*] Using device: {self.device}")
        print(f"[*] Model path: {self.MODEL_PATH}")

        if not os.path.exists(self.MODEL_PATH):
            print(f"[!] ERROR: Model not found at {self.MODEL_PATH}")
            self.model = None
            return

        try:
            self.model = YOLO(self.MODEL_PATH)
            print("[*] Plate Detector initialized successfully")
        except Exception as e:
            print(f"[!] Failed to load YOLO model: {e}")
            self.model = None

    def detect_and_crop(self, image_path):
        create_dirs()

        crops_dir = PATHS["CROPS"]
        detect_dir = PATHS["DETECTIONS"]

        os.makedirs(crops_dir, exist_ok=True)
        os.makedirs(detect_dir, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(image_path))[0]

        img = cv2.imread(image_path)

        if img is None:
            return [], None

        img_annotated = img.copy()
        h, w = img.shape[:2]

        detect_name = f"{base_name}_detected.jpg"
        detect_path = os.path.join(detect_dir, detect_name)

        if self.model is None:
            cv2.imwrite(detect_path, img_annotated)
            return [], detect_path

        results = self.model.predict(
            source=image_path,
            conf=0.10,
            imgsz=960,
            device=self.device,
            verbose=False
        )

        crops = []

        for i, r in enumerate(results):
            if r.boxes is None or len(r.boxes) == 0:
                continue

            boxes = r.boxes.xyxy.cpu().numpy()
            confs = r.boxes.conf.cpu().numpy() if r.boxes.conf is not None else []

            for j, box in enumerate(boxes):
                x1, y1, x2, y2 = map(int, box[:4])

                box_w = x2 - x1
                box_h = y2 - y1

                # reject tiny false boxes
                if box_w < 40 or box_h < 15:
                    continue

                cv2.rectangle(
                    img_annotated,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                label = "PLATE"

                if len(confs) > j:
                    label = f"PLATE {confs[j]:.2f}"

                cv2.putText(
                    img_annotated,
                    label,
                    (x1, max(25, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

                # stronger margin for OCR
                pad_x = max(10, int(box_w * 0.12))
                pad_y = max(8, int(box_h * 0.18))

                x1_final = max(0, x1 - pad_x)
                y1_final = max(0, y1 - pad_y)
                x2_final = min(w, x2 + pad_x)
                y2_final = min(h, y2 + pad_y)

                crop = img[y1_final:y2_final, x1_final:x2_final]

                if crop is None or crop.size == 0:
                    continue

                crop_name = f"{base_name}_plate_{i}_{j}.jpg"
                crop_path = os.path.join(crops_dir, crop_name)

                cv2.imwrite(crop_path, crop)

                crops.append({
                    "path": crop_path,
                    "box": [x1, y1, x2, y2],
                    "confidence": float(confs[j]) if len(confs) > j else None
                })

        cv2.imwrite(detect_path, img_annotated)

        if not crops:
            print("[*] No plates detected by YOLO.")
            return [], detect_path

        print(f"[*] YOLO detected {len(crops)} plate candidate(s).")
        return crops, detect_path