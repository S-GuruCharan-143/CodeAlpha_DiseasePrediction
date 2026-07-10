import React from 'react';
import { Link } from 'react-router-dom';

export const Home: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-16 text-center space-y-8">

      <div className="space-y-4">
        <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight sm:text-5xl">
          Heart Disease Prediction
        </h1>

        <p className="text-xl text-slate-600 max-w-2xl mx-auto">
          Predict the likelihood of heart disease using a Machine Learning model
          trained on clinical patient data.
        </p>
      </div>

      <div className="flex justify-center">
        <Link
          to="/predict"
          className="bg-slate-900 text-white px-8 py-3 rounded-md hover:bg-slate-800 transition duration-150 font-medium text-base shadow-sm"
        >
          Start Prediction
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 pt-8">

        <div className="p-6 bg-white border border-slate-200 rounded-lg text-left">
          <h3 className="text-lg font-semibold text-slate-900">
            Machine Learning Model
          </h3>

          <p className="text-sm text-slate-600 mt-2">
            Random Forest classifier trained on a Heart Disease dataset for fast
            and reliable predictions.
          </p>
        </div>

        <div className="p-6 bg-white border border-slate-200 rounded-lg text-left">
          <h3 className="text-lg font-semibold text-slate-900">
            Instant Prediction
          </h3>

          <p className="text-sm text-slate-600 mt-2">
            Get immediate prediction results along with confidence score and
            risk level.
          </p>
        </div>

        <div className="p-6 bg-white border border-slate-200 rounded-lg text-left">
          <h3 className="text-lg font-semibold text-slate-900">
            Clinical Parameters
          </h3>

          <p className="text-sm text-slate-600 mt-2">
            Uses 13 important medical parameters such as age, cholesterol,
            blood pressure, ECG, chest pain type and more.
          </p>
        </div>

      </div>

    </div>
  );
};

export default Home;