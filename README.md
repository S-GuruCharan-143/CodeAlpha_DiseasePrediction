# Credit Scoring Prediction

A full-stack machine learning web application that predicts credit risk using a Random Forest classifier trained on the German Credit Dataset. Users can submit applicant information through a modern React frontend and receive real-time credit risk predictions from a FastAPI backend.

---

## Tech Stack

| Layer        | Technology                                      |
| ------------ | ----------------------------------------------- |
| **Backend**  | Python 3.10+, FastAPI, Uvicorn, scikit-learn    |
| **Frontend** | React 18, Vite, JavaScript                      |
| **ML Model** | Random Forest Classifier (scikit-learn)          |
| **Data**     | German Credit Dataset (1,000 records)            |

---

## Project Structure

```
CreditScoring/
├── backend/
│   ├── app/
│   │   ├── api/              # API route definitions
│   │   ├── core/             # Config, security, and global settings
│   │   ├── ml/               # ML-specific logic (inference, processing)
│   │   ├── schemas/          # Pydantic request/response models
│   │   ├── services/         # Business logic and coordination
│   │   └── main.py           # FastAPI application entry point
│   └── requirements.txt      # Python dependencies
├── frontend/                 # React + Vite frontend
├── datasets/
│   └── german_credit_data.csv
├── saved_models/
│   ├── random_forest_model.joblib
│   └── preprocessor.joblib
├── scripts/
│   └── train.py              # Model training script
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

# 2. Install Python dependencies
pip install -r backend/requirements.txt

# 3. Train the model (from project root)
python scripts/train.py

# 4. Start the backend server
uvicorn backend.app.main:app --reload --port 8000
```

### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173` and the backend API at `http://localhost:8000`.

---

## API Documentation

Once the backend is running, interactive API docs are available at:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Endpoints

| Method | Endpoint       | Description                          |
| ------ | -------------- | ------------------------------------ |
| `GET`  | `/`            | Health check / welcome message       |
| `GET`  | `/health`      | API health status                    |
| `POST` | `/predict`     | Submit applicant data for prediction |

### Example Request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "sex": "male",
    "job": 2,
    "housing": "own",
    "saving_accounts": "moderate",
    "checking_account": "little",
    "credit_amount": 5000,
    "duration": 24,
    "purpose": "car"
  }'
```

### Example Response

```json
{
  "prediction": "good",
  "probability": {
    "good": 0.87,
    "bad": 0.13
  },
  "risk_score": 87
}
```

---

## Model Details

- **Algorithm:** Random Forest Classifier (100 estimators)
- **Preprocessing:** StandardScaler for numerical features, OneHotEncoder for categorical features
- **Training Split:** 80/20 with stratification
- **Dataset:** German Credit Dataset (1,000 samples, 10 features)

---

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2026 Credit Scoring Prediction

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
