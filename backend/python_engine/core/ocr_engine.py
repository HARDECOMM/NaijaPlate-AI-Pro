import os
import cv2
import numpy as np
from PIL import Image

# ✅ Use Render / system environment variables directly
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# --- INITIALIZE GEMINI ---
USING_NEW_SDK = False
_client = None
_genai_model = None


def get_gemini_instance():
    global _client, _genai_model, USING_NEW_SDK

    if _client or _genai_model:
        return _client if USING_NEW_SDK else _genai_model

    if not GEMINI_KEY:
        print("[!] GEMINI_API_KEY not found in environment")
        return None

    try:
        # NEW SDK (google-genai)
        from google import genai
        if hasattr(genai, 'Client'):
            _client = genai.Client(api_key=GEMINI_KEY)
            USING_NEW_SDK = True
            return _client
    except (ImportError, AttributeError, ValueError):
        pass

    try:
        # OLD SDK fallback
        import google.generativeai as google_genai
        google_genai.configure(api_key=GEMINI_KEY)
        _genai_model = google_genai.GenerativeModel('gemini-1.5-flash')
        USING_NEW_SDK = False
        return _genai_model
    except Exception as e:
        print(f"[!] Gemini init failed: {e}")
        return None


def load_ocr():
    import easyocr
    return easyocr.Reader(['en'])


def preprocess_for_night(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return image_path

    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    avg_brightness = np.mean(yuv[:, :, 0])

    if avg_brightness < 90:
        print(f"[*] Night detected ({avg_brightness:.2f}). Enhancing...")
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        yuv[:, :, 0] = clahe.apply(yuv[:, :, 0])
        enhanced_img = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)

        enhanced_path = image_path.replace(".jpg", "_night_enhanced.jpg")
        cv2.imwrite(enhanced_path, enhanced_img)
        return enhanced_path

    return image_path


def perform_standard_ocr(image_path, reader):
    try:
        img = cv2.imread(image_path)
        if img is None:
            return ""

        results = reader.readtext(img)
        return " ".join([res[1] for res in results]).strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""


def ai_refine_ocr(image_path):
    instance = get_gemini_instance()

    if not instance:
        print("[!] Gemini not initialized. Skipping AI refinement.")
        return "{}"

    try:
        img = Image.open(image_path)

        prompt = (
            "You are a professional license plate reader specialized in Nigerian Plates. "
            "Extract:\n"
            "1. State (top text)\n"
            "2. Number (center code like ABC-123XY)\n"
            "3. Slogan (bottom text)\n\n"
            "Return ONLY JSON:\n"
            "{ \"state\": \"...\", \"number\": \"...\", \"slogan\": \"...\" }"
        )

        model_names = [
            "gemini-3-flash-preview",
            "gemini-2.0-flash-exp",
            "gemini-3-pro-preview"
        ]

        last_error = None

        for model_name in model_names:
            try:
                if USING_NEW_SDK:
                    response = instance.models.generate_content(
                        model=model_name,
                        contents=[prompt, img]
                    )
                    text = response.text.strip()
                else:
                    import google.generativeai as google_genai
                    temp_model = google_genai.GenerativeModel(model_name)
                    response = temp_model.generate_content([prompt, img])
                    text = response.text.strip()

                if text:
                    # Clean markdown wrappers
                    if text.startswith("```"):
                        text = text.replace("```json", "").replace("```", "").strip()

                    if "{" in text and "}" in text:
                        return text

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