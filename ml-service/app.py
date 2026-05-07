import os
import uuid
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv()

from python_engine.config.paths import PATHS, create_dirs
from python_engine.core.pipeline import run_pipeline
from python_engine.core.video_pipeline import process_video


app = FastAPI(title="NaijaPlate ML Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.getcwd(), "runtime_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
create_dirs()


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "NaijaPlate ML Service",
        "message": "YOLO/OCR service is running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_path": PATHS["MODEL"],
        "model_exists": os.path.exists(PATHS["MODEL"]),
        "uploads_dir": UPLOAD_DIR,
        "output_dir": PATHS["OUTPUT"],
    }


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename or "")[1]

    if not ext:
        ext = ".mp4" if file.content_type and file.content_type.startswith("video/") else ".jpg"

    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        content_type = file.content_type or ""
        is_video = content_type.startswith("video/")

        if is_video:
            result = process_video(
                video_path=file_path,
                sample_rate=15,
                start_frame=35,
                max_frames=None,
            )
            mode = "video"
        else:
            # Fast default: no Gemini during normal analysis
            result = run_pipeline(
                input_image=file_path,
                skip_ai=True,
                verbose=False,
            )
            mode = "image"

        return {
            "status": "success",
            "mode": mode,
            "data": result,
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
        }

    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass


@app.post("/analyze-refined")
async def analyze_refined(file: UploadFile = File(...)):
    """
    Optional endpoint: slower, uses Gemini refinement.
    Use this only when user clicks 'Refine with AI'.
    """
    ext = os.path.splitext(file.filename or "")[1] or ".jpg"
    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = run_pipeline(
            input_image=file_path,
            skip_ai=False,
            verbose=False,
        )

        return {
            "status": "success",
            "mode": "image",
            "data": result,
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
        }

    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass