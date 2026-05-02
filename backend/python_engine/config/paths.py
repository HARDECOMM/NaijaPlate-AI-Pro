import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

PATHS = {
    "MODEL": os.path.join(BASE_DIR, "models", "best.pt"),
    "INPUT": os.path.join(BASE_DIR, "data", "input"),
    "OUTPUT": os.path.join(BASE_DIR, "data", "output"),
    "CROPS": os.path.join(BASE_DIR, "data", "output", "cropped"),
    "RESULTS": os.path.join(BASE_DIR, "data", "output", "results"),
}