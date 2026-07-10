import axios from 'axios';
import { DiseaseInput, PredictionResult } from '../types/credit';

const api = axios.create({
  baseURL: '/api',
});

interface DiseasePredictionResponse {
  prediction: 'Healthy' | 'Disease';
  confidence: number;
  risk: 'Low' | 'High';
}

interface HealthResponse {
  status: string;
  model_loaded: boolean;
  preprocessor_loaded: boolean;
}

function mapPredictionResponse(
  data: DiseasePredictionResponse
): PredictionResult {
  return {
    prediction: data.prediction,
    confidence: data.confidence,
    risk_level: data.risk === 'Low' ? 'Low Risk' : 'High Risk',
  };
}

export const predictDisease = async (
  data: DiseaseInput
): Promise<PredictionResult> => {
  const response = await api.post<DiseasePredictionResponse>(
    '/predict',
    data
  );

  return mapPredictionResponse(response.data);
};

export const checkHealth = async () => {
  const response = await api.get<HealthResponse>('/health');
  return response.data;
};

export default api;