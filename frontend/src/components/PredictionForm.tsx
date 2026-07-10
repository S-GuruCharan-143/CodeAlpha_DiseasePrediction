import React, { useState } from "react";
import { DiseaseInput } from "../types/credit";

interface PredictionFormProps {
  onSubmit: (data: DiseaseInput) => void;
}

const PredictionForm: React.FC<PredictionFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState<DiseaseInput>({
    age: 52,
    sex: 1,
    cp: 0,
    trestbps: 125,
    chol: 212,
    fbs: 0,
    restecg: 1,
    thalach: 168,
    exang: 0,
    oldpeak: 1.0,
    slope: 2,
    ca: 2,
    thal: 3,
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: name === "oldpeak" ? parseFloat(value) : Number(value),
    }));
  };

  const numberField = (
    label: string,
    name: keyof DiseaseInput,
    min?: number,
    max?: number
  ) => (
    <div>
      <label className="block text-sm font-medium text-slate-700 mb-1">
        {label}
      </label>

      <input
        type="number"
        name={name}
        value={formData[name]}
        min={min}
        max={max}
        step={name === "oldpeak" ? "0.1" : "1"}
        onChange={handleChange}
        className="w-full px-3 py-2 border border-slate-300 rounded-md"
      />
    </div>
  );

  const selectField = (
    label: string,
    name: keyof DiseaseInput,
    options: { value: number; label: string }[]
  ) => (
    <div>
      <label className="block text-sm font-medium text-slate-700 mb-1">
        {label}
      </label>

      <select
        name={name}
        value={formData[name]}
        onChange={handleChange}
        className="w-full px-3 py-2 border border-slate-300 rounded-md bg-white"
      >
        {options.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </select>
    </div>
  );

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(formData);
      }}
      className="space-y-6 max-w-3xl mx-auto p-6 bg-white rounded-lg border"
    >
      <h2 className="text-2xl font-semibold">
        Heart Disease Prediction
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

        {numberField("Age", "age", 1, 120)}

        {selectField("Sex", "sex", [
          { value: 1, label: "Male" },
          { value: 0, label: "Female" },
        ])}

        {selectField("Chest Pain Type", "cp", [
          { value: 0, label: "0" },
          { value: 1, label: "1" },
          { value: 2, label: "2" },
          { value: 3, label: "3" },
        ])}

        {numberField("Resting Blood Pressure", "trestbps")}

        {numberField("Cholesterol", "chol")}

        {selectField("Fasting Blood Sugar", "fbs", [
          { value: 0, label: "No" },
          { value: 1, label: "Yes" },
        ])}

        {selectField("Rest ECG", "restecg", [
          { value: 0, label: "0" },
          { value: 1, label: "1" },
          { value: 2, label: "2" },
        ])}

        {numberField("Maximum Heart Rate", "thalach")}

        {selectField("Exercise Angina", "exang", [
          { value: 0, label: "No" },
          { value: 1, label: "Yes" },
        ])}

        {numberField("Old Peak", "oldpeak")}

        {selectField("Slope", "slope", [
          { value: 0, label: "0" },
          { value: 1, label: "1" },
          { value: 2, label: "2" },
        ])}

        {selectField("Major Vessels", "ca", [
          { value: 0, label: "0" },
          { value: 1, label: "1" },
          { value: 2, label: "2" },
          { value: 3, label: "3" },
          { value: 4, label: "4" },
        ])}

        {selectField("Thal", "thal", [
          { value: 0, label: "0" },
          { value: 1, label: "1" },
          { value: 2, label: "2" },
          { value: 3, label: "3" },
        ])}

      </div>

      <button
        type="submit"
        className="w-full bg-slate-900 text-white py-3 rounded-md hover:bg-slate-800"
      >
        Predict Heart Disease
      </button>
    </form>
  );
};

export default PredictionForm;