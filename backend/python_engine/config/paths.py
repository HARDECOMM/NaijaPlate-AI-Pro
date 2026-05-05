import os

PYTHON_ENGINE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.abspath(os.path.join(PYTHON_ENGINE_DIR, ".."))

PATHS = {
    "MODEL": os.path.join(PYTHON_ENGINE_DIR, "models", "best.pt"),
    "UPLOADS": os.path.join(BACKEND_DIR, "data", "uploads"),
    "OUTPUT": os.path.join(BACKEND_DIR, "data", "output"),
    "DETECTIONS": os.path.join(BACKEND_DIR, "data", "output", "detections"),
    "CROPS": os.path.join(BACKEND_DIR, "data", "output", "cropped"),
    "PREPROCESSED": os.path.join(BACKEND_DIR, "data", "output", "preprocessed"),
    "RESULTS": os.path.join(BACKEND_DIR, "data", "output", "results"),
}


def create_dirs():
    for key, folder in PATHS.items():
        if key == "MODEL":
            continue
        os.makedirs(folder, exist_ok=True)