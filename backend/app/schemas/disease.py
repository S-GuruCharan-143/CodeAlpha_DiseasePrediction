from pydantic import BaseModel, Field


class DiseaseInput(BaseModel):
    age: int = Field(..., ge=1, le=120)
    sex: int = Field(..., ge=0, le=1)
    cp: int = Field(..., ge=0, le=3)
    trestbps: int = Field(..., gt=0)
    chol: int = Field(..., gt=0)
    fbs: int = Field(..., ge=0, le=1)
    restecg: int = Field(..., ge=0, le=2)
    thalach: int = Field(..., gt=0)
    exang: int = Field(..., ge=0, le=1)
    oldpeak: float = Field(..., ge=0)
    slope: int = Field(..., ge=0, le=2)
    ca: int = Field(..., ge=0, le=4)
    thal: int = Field(..., ge=0, le=3)


class DiseasePrediction(BaseModel):
    prediction: str
    confidence: float
    risk: str