# 🚗 NaijaPlate AI Pro

AI-powered Nigerian license plate detection and recognition system.

---

## 🔍 Overview

NaijaPlate AI Pro is a localized computer vision system designed to detect and recognize Nigerian vehicle license plates. It combines a fine-tuned YOLOv8 model, OCR, and Google Gemini multimodal AI to deliver accurate and reliable results even under challenging real-world conditions.

---

## ❗ Problem

Vehicle identification in Nigeria is largely manual, slow, and error-prone. Generic OCR systems struggle with Nigerian plate formats, lighting conditions, and environmental noise. This leads to incorrect plate readings, wrong state inference, and unreliable automation.

---

## ✅ Solution

NaijaPlate AI Pro introduces a **multi-stage intelligent pipeline**:

- 🎯 YOLOv8 (best.pt) — Detects license plates  
- ✂️ ROI Cropping — Isolates plate region  
- 🔤 EasyOCR — Extracts raw text (noisy)  
- 🤖 Gemini AI — Refines and corrects OCR output  
- 📍 Validation Engine — Applies Nigerian rules (prefix + slogan + format)  
- 📊 Confidence Scoring — Determines final reliability  

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

---

### 2️⃣ Plate Detection
![Detection](docs/demo_images/detection.jpg)

> YOLOv8 detects the plate using bounding box localization

---

### 3️⃣ Plate Crop (ROI)
![Crop](docs/demo_images/crop.jpg)

> Extracted region of interest for focused processing

---

### 4️⃣ Intelligent JSON Output

> ⚠️ This example shows a **real OCR failure corrected by AI**

```json
{
  "plate": "YAB-652CH",
  "final_state": "ABUJA",
  "confidence": "HIGH_CONFIDENCE_AI",

  "sources": {
    "ocr_raw": "0 auuin Yab6s2CH",
    "ocr_interpretation": {
      "state": "LAGOS",
      "area": "Yaba",
      "note": "Incorrect due to OCR prefix misinterpretation"
    },
    "gemini_output": {
      "state": "ABUJA",
      "number": "YAB-652CH",
      "slogan": "CENTRE OF UNITY"
    }
  },

  "decision": {
    "final_state_source": "gemini_output",
    "reason": "Gemini corrected OCR error using contextual knowledge"
  }
}

```
---

### 5️⃣ OCR Extraction (Raw Layer)

> This is the **initial OCR output**, which may contain noise and misclassifications.


```
Example:

0 auuin Yab6s2CH

⚠️ Common OCR Errors:
- `0 ↔ O`
- `2 ↔ Z`
- `1 ↔ I`
- `5 ↔ S`

⚠️ In this case:

"YAB" was misinterpreted as Lagos (Yaba)
Leading to incorrect state inference

```

---

### 6️⃣ Gemini AI Refinement

- Context understanding
- Character correction
- Nigerian plate format validation
- State + slogan consistency

```
Example Transformation:

Raw OCR:        Yab6s2CH  
Refined Output: YAB-652CH  
Correct State:  ABUJA

```

💡 Gemini identified that:

The slogan "CENTRE OF UNITY" belongs to ABUJA, not Lagos
Therefore corrected the state despite OCR ambiguity"

---

### 7️⃣ Final Output (User View)

✔ Clean plate number
✔ Correct state inferred (ABUJA)
✔ OCR errors corrected
✔ Confidence score assigned
✔ Ready for real-world use

---

### 🔄 Pipeline Flow
Input → Detection → Crop → OCR → Gemini → Validation → Output

---

---
🧠 Key Insight

OCR alone is not reliable for real-world deployment

This system improves accuracy by:

- Combining Computer Vision (YOLO)
- With OCR extraction
- And Generative AI reasoning (Gemini)

👉 Result: Robust, production-ready plate recognition system
---

## 📸 Demo

### Full Workflow

| Stage | Result |
|------|--------|
| Input | ![](docs/demo_images/input.jpg) |
| Detection | ![](docs/demo_images/detection.jpg) |
| Crop | ![](docs/demo_images/crop.jpg) |
| JSON Result | YAB-652CH, LAGOS, Yaba, CENTRE OF EXCELLENCE, HIGH_CONFIDENCE_AI|


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