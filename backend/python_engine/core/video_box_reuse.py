import cv2
import os


def extract_reused_plate_crops(model, input_dir, crop_dir, reuse_window=10):
    """
    Extracts plate crops from image sequence with temporal bounding box reuse.
    """

    os.makedirs(crop_dir, exist_ok=True)

    files = sorted(os.listdir(input_dir))

    last_box = None
    reuse_count = 0
    records = []

    for f in files:

        img_path = os.path.join(input_dir, f)
        img = cv2.imread(img_path)

        if img is None:
            continue

        # -------------------------
        # YOLO inference
        # -------------------------
        results = model.predict(img, conf=0.25, verbose=False)

        box = None

        # -------------------------
        # 1. Try fresh detection
        # -------------------------
        if results and results[0].boxes is not None and len(results[0].boxes) > 0:

            boxes = results[0].boxes.xyxy.cpu().numpy()

            # pick highest confidence box if available
            box = boxes[0]

            last_box = box
            reuse_count = 0

        # -------------------------
        # 2. Reuse last box if valid
        # -------------------------
        elif last_box is not None and reuse_count < reuse_window:
            box = last_box
            reuse_count += 1

        else:
            last_box = None
            reuse_count = 0
            continue

        # -------------------------
        # 3. Safe crop extraction
        # -------------------------
        x1, y1, x2, y2 = map(int, box)

        h, w = img.shape[:2]

        # clamp coordinates (VERY IMPORTANT)
        x1 = max(0, min(x1, w - 1))
        x2 = max(0, min(x2, w - 1))
        y1 = max(0, min(y1, h - 1))
        y2 = max(0, min(y2, h - 1))

        if x2 <= x1 or y2 <= y1:
            continue

        crop = img[y1:y2, x1:x2]

        if crop.size == 0:
            continue

        # -------------------------
        # 4. Save crop
        # -------------------------
        crop_path = os.path.join(crop_dir, f"crop_{f}")
        cv2.imwrite(crop_path, crop)

        records.append({
            "image_name": f,
            "crop_path": crop_path,
            "box": [x1, y1, x2, y2],
            "reused": reuse_count > 0
        })

    return records