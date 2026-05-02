import os

ENV = os.getenv("APP_ENV", "dev")

SETTINGS = {
    "DEBUG": ENV == "dev",
    "USE_GEMINI": True,
    "CONFIDENCE_THRESHOLD": 0.5,
}