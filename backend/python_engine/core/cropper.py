import os
import cv2


def crop_detected_plates(model, image_files, input_dir, crop_dir):

    os.makedirs(crop_dir, exist_ok=True)

    records = []

    for image_name in image_files:

        image_path = os.path.join(input_dir, image_name)
        image = cv2.imread(image_path)

        if image is None:
            continue

        # -------------------------
        # YOLO inference (balanced settings)
        # -------------------------
        result = model.predict(
            source=image_path,
            conf=0.25,          # FIXED: reduce false positives
            imgsz=960,
            device=0 if hasattr(model, "device") else "cpu",
            verbose=False
        )

        boxes = result[0].boxes

        if boxes is None or len(boxes) == 0:
            continue

        h, w = image.shape[:2]

        # -------------------------
        # iterate detections
        # -------------------------
        for i, box in enumerate(boxes):

            # confidence filter
            conf = float(box.conf[0]) if hasattr(box, "conf") else 0
            if conf < 0.25:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # -------------------------
            # validate geometry
            # -------------------------
            if x2 <= x1 or y2 <= y1:
                continue

            # -------------------------
            # adaptive padding (IMPORTANT FIX)
            # -------------------------
            box_w = x2 - x1
            box_h = y2 - y1

            pad_x = int(box_w * 0.15)
            pad_y = int(box_h * 0.25)

            x1 = max(0, x1 - pad_x)
            y1 = max(0, y1 - pad_y)
            x2 = min(w, x2 + pad_x)
            y2 = min(h, y2 + pad_y)

            crop = image[y1:y2, x1:x2]

            if crop is None or crop.size == 0:
                continue

            # -------------------------
            # optional filter: reject non-plate shapes
            # -------------------------
            aspect_ratio = (x2 - x1) / (y2 - y1 + 1e-6)

            # Nigerian plates are usually wide rectangles
            if aspect_ratio < 1.5 or aspect_ratio > 6:
                continue

            # -------------------------
            # save crop
            # -------------------------
            base = os.path.splitext(image_name)[0]
            crop_name = f"{base}_crop_{i}.jpg"
            crop_path = os.path.join(crop_dir, crop_name)

            cv2.imwrite(crop_path, crop)

            records.append({
                "image_name": image_name,
                "crop_name": crop_name,
                "crop_path": crop_path,
                "confidence": conf
            })

    return records