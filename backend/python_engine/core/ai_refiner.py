import google.generativeai as genai
from PIL import Image
import json
import re


class GeminiVerifier:

    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def _clean_json(self, text):
        """
        Extract JSON even if Gemini returns markdown or extra text.
        """
        try:
            # Remove markdown code blocks
            text = re.sub(r"```json|```", "", text).strip()

            # Extract JSON block if mixed text exists
            start = text.find("{")
            end = text.rfind("}") + 1

            if start != -1 and end != -1:
                text = text[start:end]

            return json.loads(text)

        except Exception:
            return {
                "status": "PARSE_ERROR",
                "raw": text
            }

    def verify_with_gemini(self, image_path):
        """
        Super Engine: Plate verification using Gemini Vision.
        """

        try:
            img = Image.open(image_path)

            # Optional safety resize (improves consistency)
            img = img.resize((1024, 1024))

            prompt = """
            Analyze this Nigerian license plate image.

            Extract:
            1. Plate number (format: ABC-123DE or similar)
            2. State name (top text)
            3. Plate type (Private, Commercial, Government)

            Rules:
            - Return ONLY valid JSON
            - No explanations
            - No markdown

            JSON format:
            {
              "number": "",
              "state": "",
              "type": ""
            }
            """

            response = self.model.generate_content([prompt, img])

            if not response or not response.text:
                return {
                    "status": "EMPTY_RESPONSE",
                    "number": "",
                    "state": "",
                    "type": ""
                }

            return self._clean_json(response.text)

        except Exception as e:
            return {
                "status": "AI_ERROR",
                "error": str(e),
                "number": "",
                "state": "",
                "type": ""
            }