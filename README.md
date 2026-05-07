---

title: NaijaPlate
emoji: 🚗
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
-------------

# 🚗 NaijaPlate AI Pro

## AI-Powered Nigerian License Plate Detection & Recognition System

NaijaPlate AI Pro is a localized AI-powered computer vision system designed to accurately detect, extract, validate, and recognize Nigerian vehicle license plates under real-world conditions.

The system combines:

* YOLOv8 Object Detection
* OCR Text Extraction
* Google Gemini AI Refinement
* Rule-Based Validation
* Confidence Scoring Engine

The result is a production-ready Nigerian Automatic Number Plate Recognition (ANPR) system optimized for local environments.

---

# 🔍 Overview

Traditional plate recognition systems struggle in Nigerian environments because of:

* Motion blur
* Low lighting
* Dirty plates
* OCR inaccuracies
* Non-standard plate positioning
* Environmental noise

NaijaPlate AI Pro introduces a layered AI pipeline that improves reliability using Computer Vision + OCR + Generative AI reasoning.

---

# ❗ Problem Statement

Vehicle identification systems in Nigeria are often:

* Manual
* Slow
* Error-prone
* Difficult to scale

Generic OCR systems fail to properly understand:

* Nigerian plate structures
* State prefixes
* Plate slogans
* Contextual corrections

This leads to:

* Incorrect detections
* Wrong state identification
* Poor automation reliability

---

# ✅ Solution

NaijaPlate AI Pro uses a multi-stage intelligent pipeline:

```text
Input → Detection → Crop → OCR → Gemini AI → Validation → Output
```

The system performs:

* Accurate plate localization
* OCR extraction
* AI-assisted correction
* Nigerian state inference
* Confidence scoring
* Structured API output

---

# 🧠 Core AI Pipeline

## 1️⃣ YOLOv8 Detection

YOLOv8 detects Nigerian license plates using trained custom weights.

Model:

```text
python_engine/models/best.pt
```

---

## 2️⃣ ROI Cropping

Detected plates are cropped into regions of interest for focused OCR processing.

---

## 3️⃣ OCR Extraction

EasyOCR extracts raw text from cropped plates.

Example raw OCR output:

```text
0 auuin Yab6s2CH
```

---

## 4️⃣ Gemini AI Refinement

Google Gemini AI intelligently refines noisy OCR results.

Example:

```text
Raw OCR:        Yab6s2CH
Refined Plate: YAB-652CH
Correct State: ABUJA
```

Gemini helps correct:

* Character confusion
* OCR distortion
* Contextual state mismatch
* Invalid formatting

---

## 5️⃣ Validation Engine

The system validates:

* Nigerian plate format
* State prefix consistency
* Plate structure
* Confidence levels

---

# 📊 Example JSON Output

```json
{
  "plate": "YAB-652CH",
  "final_state": "ABUJA",
  "confidence": "HIGH_CONFIDENCE_AI",

  "sources": {
    "ocr_raw": "0 auuin Yab6s2CH",
    "gemini_output": {
      "state": "ABUJA",
      "number": "YAB-652CH"
    }
  }
}
```

---

# 🧠 Key Features

* 🇳🇬 Nigerian plate localization
* 🤖 AI-powered OCR correction
* 📍 Prefix-based state inference
* 📊 Confidence scoring
* 📦 Structured JSON API output
* 🎥 Image & Video support
* ⚡ Real-time inference architecture
* ☁️ Cloud-deployed ML inference service

---

# 🧩 Production Deployment Architecture

NaijaPlate AI Pro uses a distributed modern AI architecture.

## 🌐 System Architecture

```text
Frontend (Vercel)
        ↓
Backend API (Render)
        ↓
ML Inference Service (Hugging Face Spaces)
```

---

# 🖥️ Frontend Deployment — Vercel

The frontend UI is deployed on Vercel.

### Responsibilities

* Upload interface
* Detection visualization
* User interaction
* API communication

### Stack

* React
* Vite
* Axios
* Tailwind CSS

---

# ⚙️ Backend Deployment — Render

The backend API orchestration layer runs on Render.

### Responsibilities

* Upload handling
* Middleware
* API orchestration
* Response formatting
* Communication with ML inference service

### Stack

* Node.js
* Express.js
* Multer
* Axios

---

# 🤖 ML Inference Deployment — Hugging Face Spaces

The ML engine is independently deployed on Hugging Face Spaces using Docker.

## 🔗 Live ML Service

https://huggingface.co/spaces/Hardecomm/NaijaPlate

## 🔗 Direct Runtime Endpoint

https://hardecomm-naijaplate.hf.space

### Responsibilities

* YOLO inference
* OCR processing
* Gemini refinement
* Video frame analysis
* Confidence scoring

### ML Stack

* Python
* YOLOv8
* EasyOCR
* OpenCV
* Google Gemini AI
* Docker

---

# ⚡ Why This Architecture?

This architecture improves:

* Scalability
* Maintainability
* ML isolation
* Deployment stability
* Real-time inference performance

Each layer can scale independently.

---

# 🔌 API Communication

## Frontend → Backend

```javascript
const API_BASE_URL =
  "https://your-render-backend.onrender.com";
```

## Backend → ML Service

```javascript
const ML_SERVICE_URL =
  "https://hardecomm-naijaplate.hf.space";
```

---

# 📡 Health Check Endpoint

The deployed ML service exposes:

```json
{
  "status":"ok",
  "service":"NaijaPlate ML Service",
  "message":"YOLO/OCR service is running"
}
```

This confirms:

* Docker deployment successful
* YOLO initialized
* OCR initialized
* ML service operational

---

# 🧠 Tech Stack

## Frontend

* React
* Vite
* Tailwind CSS

## Backend

* Node.js
* Express.js

## AI & ML

* YOLOv8
* EasyOCR
* Google Gemini AI
* OpenCV

## Deployment

* Vercel
* Render
* Hugging Face Spaces
* Docker

---

# 📂 Project Structure

```text
NaijaPlate/
│
├── frontend/
│
├── backend/
│
├── ml-service/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   │
│   └── python_engine/
│       ├── core/
│       ├── config/
│       ├── models/
│       │   └── best.pt
│       └── main.py
│
└── README.md
```

---

# 🚀 Real-World Applications

NaijaPlate AI Pro can support:

* 🚓 Law enforcement systems
* 🚦 Smart traffic systems
* 🏢 Estate gate automation
* 📦 Logistics verification
* 🅿️ Smart parking systems
* 🚘 Vehicle verification platforms

---

# ⚠️ Current Challenges

* Motion blur
* Night-time inference
* OCR inconsistencies
* Frame instability in videos

---

# 🔮 Future Improvements

* Multi-frame voting
* Real-time CCTV integration
* GPU optimization
* Vehicle re-identification
* Traffic analytics dashboard
* Async inference queues
* Multi-camera processing

---

# 👤 Author

## Haruna Adegoke Ademoye

AI/ML Engineer • Computer Vision Engineer • Backend Developer

📍 Lagos, Nigeria

### LinkedIn

https://linkedin.com/in/haruna-ademoye-859486110

### Portfolio

https://professiona-portfolio.netlify.app/

---

# 💡 Final Note

NaijaPlate AI Pro demonstrates how localized AI systems can solve real-world African mobility and surveillance problems using:

```text
Computer Vision + OCR + Generative AI
```

This project represents a strong foundation for:

* Smart city systems
* AI surveillance
* Intelligent transportation
* Automated vehicle verification
* Real-time Nigerian ANPR infrastructure
