# 🚗 NaijaPlate AI Pro

AI-powered Nigerian license plate detection and recognition system.

---

## 🔍 Overview

NaijaPlate AI Pro is a localized computer vision system designed to accurately detect and recognize Nigerian vehicle license plates. It combines a fine-tuned YOLOv8 model, OCR, and Google Gemini multimodal AI to deliver high-accuracy results even under challenging real-world conditions.

---

## ❗ Problem

Vehicle identification in Nigeria is largely manual, slow, and error-prone. Security personnel rely on human logging, leading to mistakes and inefficiencies. Generic OCR systems fail due to Nigerian plate formats, lighting variations, and environmental noise.

---

## ✅ Solution

NaijaPlate AI Pro introduces a multi-stage intelligent pipeline:

- 🎯 YOLOv8 (best.pt) — Plate detection  
- ✂️ ROI Cropping — Remove background noise  
- 🔤 EasyOCR — Extract raw text  
- 🤖 Gemini AI — Correct OCR errors  
- 📍 Prefix Validation — Map to State & LGA  
- 📊 Confidence Scoring — Reliability assessment  

---

## 🧩 System Architecture

![Architecture](docs/architecture.png)

---

## 🧠 Layered Pipeline

![Layered Pipeline](docs/layered.png)

---

## 🤖 OCR + Gemini Enhancement

![OCR Enhancement](docs/ocr_enhancement.png)

---

## ⚙️ How It Works (Step-by-Step)

### 1️⃣ Input Image
![Input](docs/demo_images/input.jpg)

### 2️⃣ Plate Detection
![Detection](docs/demo_images/detection.jpg)

### 3️⃣ Plate Crop
![Crop](docs/demo_images/crop.jpg)

### 4️⃣ Final JSON Result
```json

{
    "plate": "YAB-652CH",
    "state": "LAGOS",
    "nickname": "CENTRE OF EXCELLENCE",
    "confidence": "HIGH_CONFIDENCE_AI",
    "standard_raw": "0 auuin Yab6s2CH",
    "ai_raw": "{\n  \"state\": \"ABUJA\",\n  \"number\": \"YAB-652CH\",\n  \"slogan\": \"CENTRE OF UNITY\"\n}",
    "used_night_mode": false,
    "is_cropped": true,
    "bounding_box": [
        262,
        478,
        381,
        586
    ],
    "annotated_detection": "C:\\Users\\ademo\\Downloads\\Projects\\PlateSightAI\\Backend\\python_engine\\data\\output\\detections\\1777759053450-923746684_detected.jpg"
}

```

---

### 5️⃣ OCR Extraction
*(Raw output may contain errors like 0/O, 2/Z, 1/I)*

---

### 6️⃣ Gemini AI Refinement
- Context understanding  
- Character correction  
- Format alignment  

---

### 7️⃣ Final Output
![Output](docs/demo_images/output.jpg)

---

### 🔄 Pipeline Flow
nput → Detection → Crop → OCR → Gemini → Validation → Output


---

## 📸 Demo

### Full Workflow

| Stage | Result |
|------|--------|
| Input | ![](docs/demo_images/input.jpg) |
| Detection | ![](docs/demo_images/detection.jpg) |
| Crop | ![](docs/demo_images/crop.jpg) |
| JSON Result | Plate number, state, area, confidence |

---

### Sample Output
Plate: GWA120CP
State: ABUJA
Area: Gwagwalada
Confidence: HIGH
Review Status: ACCEPT



---

## 🧠 Key Features

- Localized Nigerian plate recognition  
- OCR error correction using AI  
- Prefix-based state & LGA inference  
- Structured JSON output  
- Scalable architecture (API-ready)  

---

## 🧠 Tech Stack

- **Backend:** Python  
- **Detection:** YOLOv8 (Ultralytics)  
- **OCR:** EasyOCR  
- **AI Refinement:** Google Gemini  
- **Frontend:** React  
- **API:** Flask / Node.js  

---

## 🚀 Real-World Impact

NaijaPlate AI Pro enables:

- 🔐 Estate security automation  
- 🚓 Law enforcement support  
- 🚦 Traffic monitoring systems  
- 📦 Logistics & fleet tracking  

It reduces manual errors and improves speed and reliability in vehicle identification systems.

---

## ⚠️ Challenges

- OCR inaccuracies (0 vs O, 2 vs Z)  
- Video frame inconsistency  
- Lighting and motion blur  

---

## 🔮 Next Steps

- Improve OCR with ensemble models  
- Add multi-frame voting for video  
- Train segmentation model for plate zones  
- Integrate real-time CCTV systems  
- Deploy scalable API  

---

## 📂 Project Structure

``
NaijaPlate-AI-Pro/
├── frontend/
├── backend/
├── models/
├── data/
├── docs/
│ ├── demo_images/
│ │ ├── input.jpg
│ │ ├── detection.jpg
│ │ ├── crop.jpg
│ │ └── results.json
│ ├── architecture.png
│ ├── layered.png
│ └── ocr_enhancement.png
├── api/
└── README.md
``

---

## 👤 Author

**Haruna Adegoke Ademoye**  
AI/ML Engineer | Computer Vision  
Lagos, Nigeria  

---

## 💡 Note

This project demonstrates how localized AI systems can solve real-world challenges by combining computer vision, OCR, and generative AI into a unified intelligent pipeline.