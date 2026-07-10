import React, { useState } from 'react';
import PredictionForm from '../components/PredictionForm';
import PredictionResult from '../components/PredictionResult';
import LoadingSpinner from '../components/LoadingSpinner';

import { predictDisease } from '../services/api';
import { DiseaseInput, PredictionResult as ResultType } from '../types/credit';

export const Predict: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ResultType | null>(null);

  const handleSubmit = async (data: DiseaseInput) => {
    setLoading(true);
    setError(null);

    try {
      const response = await predictDisease(data);
      setResult(response);
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
        err.message ||
        "Prediction failed."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">

      <div className="text-center mb-8">
        <h1 className="text-3xl font-extrabold text-slate-900 sm:text-4xl">
          Heart Disease Prediction
        </h1>

        <p className="text-slate-600 mt-2">
          Enter the patient's clinical information to predict the likelihood of heart disease.
        </p>
      </div>

      {loading && <LoadingSpinner />}

      {!loading && error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded">
          {error}

          <button
            className="block mt-3 underline"
            onClick={handleReset}
          >
            Try Again
          </button>
        </div>
      )}

      {!loading && !error && !result && (
        <PredictionForm onSubmit={handleSubmit} />
      )}

      {!loading && !error && result && (
        <PredictionResult
          result={result}
          onReset={handleReset}
        />
      )}

    </div>
  );
};

export default Predict;