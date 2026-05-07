import os

PYTHON_ENGINE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

ML_SERVICE_DIR = os.path.abspath(
    os.path.join(PYTHON_ENGINE_DIR, "..")
)

DATA_DIR = os.path.join(ML_SERVICE_DIR, "data")
OUTPUT_DIR = os.path.join(DATA_DIR, "output")

PATHS = {
    "MODEL": os.path.join(PYTHON_ENGINE_DIR, "models", "best.pt"),

    "OUTPUT": OUTPUT_DIR,

    "DETECTIONS": os.path.join(OUTPUT_DIR, "detections"),

    "CROPS": os.path.join(OUTPUT_DIR, "cropped"),

    "PREPROCESSED": os.path.join(OUTPUT_DIR, "preprocessed"),

    "RESULTS": os.path.join(OUTPUT_DIR, "results"),
}


def create_dirs():
    for key, folder in PATHS.items():
        if key == "MODEL":
            continue

        os.makedirs(folder, exist_ok=True)