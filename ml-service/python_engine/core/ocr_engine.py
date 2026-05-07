import os
import cv2
import json
from PIL import Image

from .plate_zone import preprocess_for_main_number


GEMINI_KEY = os.getenv("GEMINI_API_KEY")

USING_NEW_SDK = False
_client = None
_genai_model = None
_reader = None


def get_gemini_instance():
    global _client, _genai_model, USING_NEW_SDK

    if _client or _genai_model:
        return _client if USING_NEW_SDK else _genai_model

    if not GEMINI_KEY:
        print("[!] GEMINI_API_KEY not found in environment")
        return None

    try:
        from google import genai

        if hasattr(genai, "Client"):
            _client = genai.Client(api_key=GEMINI_KEY)
            USING_NEW_SDK = True
            return _client
    except Exception:
        pass

    try:
        import google.generativeai as google_genai

        google_genai.configure(api_key=GEMINI_KEY)
        _genai_model = google_genai.GenerativeModel("gemini-1.5-flash")
        USING_NEW_SDK = False
        return _genai_model

    except Exception as e:
        print(f"[!] Gemini init failed: {e}")
        return None


def load_ocr():
    global _reader

    if _reader is not None:
        return _reader

    import easyocr

    _reader = easyocr.Reader(["en"], gpu=False)
    return _reader


def preprocess_for_night(image_path):
    """
    Kept for backward compatibility with pipeline.py.
    Internally uses improved plate preprocessing.
    """
    return preprocess_for_main_number(image_path)


def perform_standard_ocr(image_path, reader=None):
    try:
        if reader is None:
            reader = load_ocr()

        img = cv2.imread(image_path)

        if img is None:
            return ""

        h, w = img.shape[:2]

        # Prevent EasyOCR CPU memory crash
        max_width = 900
        if w > max_width:
            scale = max_width / w
            img = cv2.resize(
                img,
                (int(w * scale), int(h * scale)),
                interpolation=cv2.INTER_AREA
            )

        results = reader.readtext(img, detail=1, paragraph=False)
        return " ".join([res[1] for res in results]).strip()

    except Exception as e:
        print(f"OCR Error: {e}")
        return ""


def clean_gemini_json(text):
    if not text:
        return "{}"

    text = str(text).strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}") + 1

    if start != -1 and end > start:
        text = text[start:end]

    try:
        data = json.loads(text)

        return json.dumps({
            "state": str(data.get("state", "")).upper(),
            "number": str(data.get("number", "")).upper(),
            "slogan": str(data.get("slogan", "")).upper()
        })

    except Exception:
        return "{}"


def ai_refine_ocr(image_path):
    """
    Kept with this exact name because pipeline.py imports ai_refine_ocr.
    """
    instance = get_gemini_instance()

    if not instance:
        print("[!] Gemini not initialized. Skipping AI refinement.")
        return "{}"

    try:
        img = Image.open(image_path)

        prompt = """
You are a professional Nigerian vehicle license plate reader.

Analyze ONLY the license plate in this image.

Extract:
1. state: the Nigerian state or FCT written on the plate
2. number: the plate number in standard format like ABC-123DE
3. slogan: the state slogan written on the plate, if visible

Rules:
- Return ONLY valid JSON
- No markdown
- No explanations
- Do not guess car brand, model, or other text
- If unsure, use empty string
- Correct OCR-like mistakes such as 0/O, 2/Z, 1/I, 5/S, 8/B only when context supports it

JSON format:
{
  "state": "",
  "number": "",
  "slogan": ""
}
"""

        model_names = [
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-flash-latest",
        ]

        last_error = None

        for model_name in model_names:
            try:
                if USING_NEW_SDK:
                    response = instance.models.generate_content(
                        model=model_name,
                        contents=[prompt, img]
                    )
                    text = response.text.strip() if response.text else ""
                else:
                    import google.generativeai as google_genai

                    temp_model = google_genai.GenerativeModel(model_name)
                    response = temp_model.generate_content([prompt, img])
                    text = response.text.strip() if response.text else ""

                cleaned = clean_gemini_json(text)

                if cleaned != "{}":
                    return cleaned

            except Exception as e:
                error_msg = str(e).upper()

                if "429" in error_msg:
                    print("[!] Gemini quota exceeded")
                    return '{"error":"quota_exceeded"}'

                last_error = e
                continue

        if last_error:
            print(f"[!] AI OCR failed: {last_error}")

        return "{}"

    except Exception as e:
        print(f"AI Refine Error: {e}")
        return "{}"