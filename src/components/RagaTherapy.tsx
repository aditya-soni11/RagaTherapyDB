import { useState } from "react";
import { recommendRaga, RecommendationResult } from "../engine/recommendationEngine";
import RagaCard from "./RagaCard";
import SupportingFactors from "./SupportingFactors";
import AlternativeRagas from "./AlternativeRagas";
import DetectedConditions from "./DetectedConditions";
import FeatureRadar from "./FeatureRadar";

const EXAMPLE_INPUTS = [
  "I have anxiety and stress",
  "I am unable to sleep",
  "I feel depressed and restless",
  "I have high stress levels",
  "I suffer from migraine pain",
  "I have hypertension and palpitations",
];

export default function RagaTherapy() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<RecommendationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!input.trim()) {
      setError("Please enter a symptom, disease, or condition description.");
      return;
    }

    setLoading(true);

    // Simulate processing delay for UX
    setTimeout(() => {
      try {
        const recommendation = recommendRaga(input.trim());
        setResult(recommendation);
      } catch (err) {
        setError("An error occurred during analysis. Please try again.");
      }
      setLoading(false);
    }, 800);
  };

  const handleExampleClick = (example: string) => {
    setInput(example);
    setError("");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-rose-50">
      {/* Header */}
      <header className="border-b border-amber-200 bg-white/70 backdrop-blur-sm">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 text-white shadow-lg shadow-amber-200">
              <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
                <path d="M9 18V5l12-2v13" />
                <circle cx="6" cy="18" r="3" />
                <circle cx="18" cy="16" r="3" />
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-800">RagaTherapy</h1>
              <p className="text-xs text-gray-500">AI-Powered Disease-Aware Raga Recommendation</p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <span className="hidden sm:inline">Indian Classical Music Therapy</span>
            <span className="text-amber-400">🎵</span>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-8">
        {/* Input Section */}
        <div className="mb-8 rounded-2xl bg-white p-6 shadow-lg shadow-amber-100/50">
          <form onSubmit={handleSubmit} className="space-y-4">
            <label className="block text-sm font-semibold text-gray-700">
              Describe your symptoms, disease, or medical condition:
            </label>
            <div className="relative">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder='e.g., "I have anxiety and stress", "Unable to sleep at night", "I feel depressed and restless"...'
                rows={3}
                className="w-full resize-none rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-gray-800 placeholder-gray-400 transition-all focus:border-amber-400 focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-200"
              />
            </div>

            {error && (
              <p className="text-sm text-red-500 flex items-center gap-1">
                <span>⚠</span> {error}
              </p>
            )}

            <div className="flex items-center gap-3">
              <button
                type="submit"
                disabled={loading}
                className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-amber-500 to-orange-600 px-6 py-2.5 text-sm font-semibold text-white shadow-md shadow-amber-200 transition-all hover:from-amber-600 hover:to-orange-700 disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                      <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeDasharray="31.4 31.4" />
                    </svg>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
                      <circle cx="11" cy="11" r="8" />
                      <path d="m21 21-4.3-4.3" />
                    </svg>
                    Recommend Raga
                  </>
                )}
              </button>

              <button
                type="button"
                onClick={() => {
                  setInput("");
                  setResult(null);
                  setError("");
                }}
                className="text-sm text-gray-400 hover:text-gray-600 transition-colors"
              >
                Clear
              </button>
            </div>
          </form>

          {/* Example inputs */}
          <div className="mt-4 flex flex-wrap gap-2">
            <span className="text-xs font-medium text-gray-400 pt-0.5">Try:</span>
            {EXAMPLE_INPUTS.map((example) => (
              <button
                key={example}
                onClick={() => handleExampleClick(example)}
                className="rounded-full bg-amber-50 px-3 py-1 text-xs text-amber-700 transition-colors hover:bg-amber-100 hover:text-amber-800"
              >
                {example}
              </button>
            ))}
          </div>
        </div>

        {/* Loading Skeleton */}
        {loading && (
          <div className="space-y-6 animate-pulse">
            <div className="h-64 rounded-2xl bg-white"></div>
            <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
              <div className="h-48 rounded-2xl bg-white"></div>
              <div className="h-48 rounded-2xl bg-white"></div>
            </div>
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            {/* Detected Conditions */}
            <DetectedConditions
              conditions={result.extracted_features.detected_conditions}
              conditionScores={result.extracted_features.condition_scores}
            />

            {/* Main Recommendation */}
            <RagaCard recommendation={result.recommended_raga} />

            {/* Two Column Layout */}
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
              {/* Supporting Factors */}
              <div className="lg:col-span-1">
                <SupportingFactors factors={result.supporting_factors} />
              </div>

              {/* Feature Radar */}
              <div className="lg:col-span-2">
                <FeatureRadar features={result.extracted_features} raga={result.recommended_raga.raga} />
              </div>
            </div>

            {/* Alternative Ragas */}
            <AlternativeRagas alternatives={result.alternative_ragas} />

            {/* Explanation */}
            <div className="rounded-2xl bg-white p-6 shadow-md">
              <h3 className="mb-3 text-lg font-semibold text-gray-800">📖 Detailed Explanation</h3>
              <p className="text-gray-600 leading-relaxed text-sm">
                {result.recommended_raga.explanation}
              </p>
            </div>
          </div>
        )}

        {/* Empty state */}
        {!result && !loading && !error && (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <div className="mb-6 flex h-24 w-24 items-center justify-center rounded-full bg-amber-100">
              <svg className="h-12 w-12 text-amber-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
                <path d="M9 18V5l12-2v13" />
                <circle cx="6" cy="18" r="3" />
                <circle cx="18" cy="16" r="3" />
              </svg>
            </div>
            <h2 className="mb-2 text-xl font-semibold text-gray-700">RagaTherapy System</h2>
            <p className="max-w-md text-sm text-gray-500">
              Enter your symptoms or condition above to receive an AI-powered
              recommendation of the most therapeutically suitable Indian Classical Raga.
              Our system analyzes disease features, emotional states, and music therapy
              research to provide personalized recommendations.
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-amber-100 bg-white/50 py-4 text-center text-xs text-gray-400">
        RagaTherapy — AI-Powered Disease-Aware Raga Recommendation System •
        Based on published music therapy literature &amp; clinical research
      </footer>
    </div>
  );
}
