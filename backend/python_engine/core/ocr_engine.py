import os
import cv2
import numpy as np
from PIL import Image
from dotenv import load_dotenv

# Load variables from .env - searching in multiple locations
load_dotenv() 
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# --- INITIALIZE GEMINI ---
# We use lazy initialization to prevent the "No API key" crash at startup
USING_NEW_SDK = False
_client = None
_genai_model = None

def get_gemini_instance():
    global _client, _genai_model, USING_NEW_SDK
    
    if _client or _genai_model:
        return _client if USING_NEW_SDK else _genai_model

    if not GEMINI_KEY:
        return None

    try:
        # Attempt NEW SDK (google-genai)
        from google import genai
        if hasattr(genai, 'Client'):
            _client = genai.Client(api_key=GEMINI_KEY)
            USING_NEW_SDK = True
            return _client
    except (ImportError, AttributeError, ValueError):
        pass

    try:
        # Fallback to OLD SDK (google-generativeai)
        import google.generativeai as google_genai
        google_genai.configure(api_key=GEMINI_KEY)
        _genai_model = google_genai.GenerativeModel('gemini-1.5-flash')
        USING_NEW_SDK = False
        return _genai_model
    except Exception:
        return None

def load_ocr():
    """
    Placeholder to maintain backward compatibility with old imports.
    """
    import easyocr
    return easyocr.Reader(['en'])

def preprocess_for_night(image_path):
    """
    Enhances dark images using CLAHE (Contrast Limited Adaptive Histogram Equalization).
    """
    img = cv2.imread(image_path)
    if img is None: return image_path
    
    # Convert to YUV to check brightness
    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    avg_brightness = np.mean(yuv[:,:,0])
    
    # If dark, enhance
    if avg_brightness < 90:
        print(f"[*] Night detected ({avg_brightness:.2f}). Enhancing...")
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        yuv[:,:,0] = clahe.apply(yuv[:,:,0])
        enhanced_img = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        
        enhanced_path = image_path.replace(".jpg", "_night_enhanced.jpg")
        cv2.imwrite(enhanced_path, enhanced_img)
        return enhanced_path
    
    return image_path

def perform_standard_ocr(image_path, reader):
    """
    Standard EasyOCR logic.
    """
    try:
        img = cv2.imread(image_path)
        if img is None: return ""
        
        results = reader.readtext(img)
        return " ".join([res[1] for res in results]).strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""

def ai_refine_ocr(image_path):
    """
    Advanced Gemini Refinement. Uses the correct SDK based on what was detected.
    """
    instance = get_gemini_instance()
    if not instance:
        print("[!] Gemini Instance not initialized. Check your .env for GEMINI_API_KEY.")
        return ""

    try:
        img = Image.open(image_path)
        # Inside ai_refine_ocr function
        prompt = (
            "You are a professional license plate reader specialized in Nigerian Plates. "
            "Examine the image and extract: "
            "1. State: The state name, usually found at the VERY TOP (e.g. LAGOS, KANO). "
            "2. Number: The main alpha-number plate code in the CENTER (Ex: KJA 456 MZ). " # CHANGED EXAMPLE
            "3. Slogan: The small state motto text at the absolute BOTTOM (Ex: 'CENTRE OF EXCELLENCE'). "
            "IMPORTANT: Return ONLY JSON: { \"state\": \"...\", \"number\": \"...\", \"slogan\": \"...\" }."
        )

        # Use the most stable and compatible model names
        model_names = ['gemini-3-flash-preview', 'gemini-2.0-flash-exp', 'gemini-3-pro-preview']
        
        last_error = None
        for model_name in model_names:
            try:
                if USING_NEW_SDK:
                    # New SDK (google.genai)
                    response = instance.models.generate_content(
                        model=model_name,
                        contents=[prompt, img]
                    )
                    text = response.text.strip()
                else:
                    # Legacy SDK (google.generativeai)
                    import google.generativeai as google_genai
                    temp_model = google_genai.GenerativeModel(model_name)
                    response = temp_model.generate_content([prompt, img])
                    text = response.text.strip()
                
                # If we get here, the request succeeded
                if text:
                    # Clean JSON if AI added markdown wrappers
                    if text.startswith("```json"):
                        text = text.replace("```json", "").replace("```", "").strip()
                    elif text.startswith("```"):
                        text = text.replace("```", "").strip()

                    if "{" in text and "}" in text:
                        return text # Return JSON string
            except Exception as e:
                error_msg = str(e).upper()
                if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    print(f"[!] Rate Limit (429) hit on model {model_name}. Skipping AI refinement for this image.")
                    return json.dumps({"status": "AI_LIMIT_REACHED", "error": "Quota Exceeded"})
                
                if "405" in error_msg:
                    print(f"[!] Warning: Model {model_name} returned 405 (Not Allowed).")
                elif "404" in error_msg:
                    print(f"[*] Note: Model {model_name} not found.")
                
                last_error = e
                continue
        
        if last_error:
            print(f"[!] AI OCR Failed. Final error: {last_error}")
        return "{}" # Return empty JSON
            
    except Exception as e:
        print(f"AI Refine Error: {e}")
        return ""
