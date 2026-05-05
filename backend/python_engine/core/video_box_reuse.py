import os
import cv2

from python_engine.config.paths import create_dirs


def extract_reused_plate_crops(
    model,
    input_dir,
    crop_dir,
    reuse_window=10,
    conf=0.10,
    imgsz=960,
    pad_x=50,
    pad_y=30,
):
    """
    Extracts plate crops from image frames using detection + temporal box reuse.
    Useful for video frames where YOLO detects one frame but misses nearby frames.
    """

    create_dirs()
    os.makedirs(crop_dir, exist_ok=True)

    files = sorted([
        f for f in os.listdir(input_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

    last_box = None
    reuse_count = 0
    records = []

    for f in files:
        img_path = os.path.join(input_dir, f)
        img = cv2.imread(img_path)

        if img is None:
            continue

        h, w = img.shape[:2]

        results = model.predict(
            source=img,
            conf=conf,
            imgsz=imgsz,
            verbose=False
        )

        box = None
        reused = False

        if results and results[0].boxes is not None and len(results[0].boxes) > 0:
            boxes = results[0].boxes.xyxy.cpu().numpy()

            # Pick first/highest confidence box
            x1, y1, x2, y2 = map(int, boxes[0][:4])

            box_w = x2 - x1
            box_h = y2 - y1

            # reject tiny false detections
            if box_w < 80 or box_h < 25:
                continue

            box = [x1, y1, x2, y2]
            last_box = box
            reuse_count = 0

        elif last_box is not None and reuse_count < reuse_window:
            box = last_box
            reuse_count += 1
            reused = True

        else:
            last_box = None
            reuse_count = 0
            continue

        x1, y1, x2, y2 = map(int, box)

        x1 = max(0, x1 - pad_x)
        y1 = max(0, y1 - pad_y)
        x2 = min(w, x2 + pad_x)
        y2 = min(h, y2 + pad_y)

        if x2 <= x1 or y2 <= y1:
            continue

        crop = img[y1:y2, x1:x2]

        if crop is None or crop.size == 0:
            continue

        crop_name = f"{os.path.splitext(f)[0]}_crop_{len(records)}.jpg"
        crop_path = os.path.join(crop_dir, crop_name)

        cv2.imwrite(crop_path, crop)

        records.append({
            "image_name": f,
            "crop_name": crop_name,
            "crop_path": crop_path,
            "path": crop_path,
            "box": [x1, y1, x2, y2],
            "reused": reused,
            "crop_source": "reused_box" if reused else "detected",
        })

    return records