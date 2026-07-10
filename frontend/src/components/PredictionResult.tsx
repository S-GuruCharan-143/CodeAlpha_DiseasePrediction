import React from "react";
import { PredictionResult as ResultType } from "../types/credit";

interface PredictionResultProps {
  result: ResultType;
  onReset: () => void;
}

const PredictionResult: React.FC<PredictionResultProps> = ({
  result,
  onReset,
}) => {
  const isHealthy = result.prediction === "Healthy";

  return (
    <div className="max-w-xl mx-auto p-6 bg-white border border-slate-200 rounded-lg text-center space-y-6">

      <div>
        <h2 className="text-xl font-bold text-slate-900">
          Prediction Result
        </h2>

        <p className="text-sm text-slate-500 mt-1">
          Based on the patient's clinical information
        </p>
      </div>

      <div className="py-4">
        <span
          className={`inline-block px-6 py-3 rounded-full text-lg font-bold tracking-wide uppercase ${
            isHealthy
              ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
              : "bg-rose-50 text-rose-700 border border-rose-200"
          }`}
        >
          {result.prediction}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4 border-t border-b border-slate-100 py-4">

        <div>
          <span className="block text-xs font-semibold uppercase tracking-wider text-slate-400">
            Risk Level
          </span>

          <span
            className={`text-sm font-medium ${
              result.risk_level === "Low Risk"
                ? "text-emerald-600"
                : "text-rose-600"
            }`}
          >
            {result.risk_level}
          </span>
        </div>

        <div>
          <span className="block text-xs font-semibold uppercase tracking-wider text-slate-400">
            Confidence
          </span>

          <span className="text-sm font-medium text-slate-900">
            {(result.confidence * 100).toFixed(1)}%
          </span>
        </div>

      </div>

      <button
        onClick={onReset}
        className="w-full bg-slate-100 text-slate-800 py-2 rounded-md hover:bg-slate-200"
      >
        Predict Another Patient
      </button>

    </div>
  );
};

export default PredictionResult;