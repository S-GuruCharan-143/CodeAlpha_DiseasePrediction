# Heart Disease Prediction System

A full-stack machine learning web application that predicts the likelihood of heart disease using a Random Forest classifier trained on a Heart Disease dataset. Users can submit patient clinical information through a modern React frontend and receive real-time disease predictions from a FastAPI backend.

---

## Tech Stack

| Layer        | Technology                                   |
| ------------ | -------------------------------------------- |
| **Backend**  | Python 3.10+, FastAPI, Uvicorn, scikit-learn |
| **Frontend** | React 18, Vite, TypeScript                   |
| **ML Model** | Random Forest Classifier (scikit-learn)      |
| **Data**     | Heart Disease Dataset (1,025 records)        |

---

## Project Structure

```
DiseasePrediction_Clean/
├── backend/
│   ├── app/
│   │   ├── api/              # API route definitions
│   │   ├── core/             # Configuration and global settings
│   │   ├── ml/               # ML preprocessing, training and inference
│   │   ├── schemas/          # Pydantic request/response models
│   │   ├── services/         # Prediction service layer
│   │   └── main.py           # FastAPI application entry point
│   └── requirements.txt
├── frontend/                 # React + Vite frontend
├── datasets/
│   └── heart_disease.csv
├── saved_models/
│   ├── random_forest_model.joblib
│   └── preprocessing_pipeline.joblib
├── backend/
│   └── app/
│       └── ml/
│           └── train.py
├── .gitignore
└── README.md
```

---

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Node.js 18+ and npm

### Backend Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Train the model
python backend/app/ml/train.py

# 4. Start the backend
uvicorn backend.app.main:app --reload --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at **http://localhost:5173** and the backend API at **http://localhost:8000**.

---

## API Documentation

After starting the backend:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | API health status |
| POST | `/predict` | Predict heart disease |

---

## Example Request

```bash
curl -X POST http://localhost:8000/predict \
-H "Content-Type: application/json" \
-d '{
  "age": 52,
  "sex": 1,
  "cp": 0,
  "trestbps": 125,
  "chol": 212,
  "fbs": 0,
  "restecg": 1,
  "thalach": 168,
  "exang": 0,
  "oldpeak": 1.0,
  "slope": 2,
  "ca": 2,
  "thal": 3
}'
```

---

## Example Response

```json
{
  "prediction": "Healthy",
  "confidence": 0.98,
  "risk": "Low"
}
```

or

```json
{
  "prediction": "Heart Disease",
  "confidence": 0.96,
  "risk": "High"
}
```

---

## Model Details

- **Algorithm:** Random Forest Classifier
- **Preprocessing:** Direct numerical feature processing (no scaling required)
- **Training Split:** 80/20 with stratified sampling
- **Dataset:** Heart Disease Dataset (1,025 samples, 13 clinical features)

### Input Features

- Age
- Sex
- Chest Pain Type
- Resting Blood Pressure
- Cholesterol
- Fasting Blood Sugar
- Resting ECG
- Maximum Heart Rate Achieved
- Exercise-Induced Angina
- ST Depression (Oldpeak)
- ST Slope
- Number of Major Vessels
- Thalassemia

### Output

- Healthy
- Heart Disease

---

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2026 Heart Disease Prediction System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```