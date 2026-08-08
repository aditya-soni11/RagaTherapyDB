import { ExtractedFeatures } from "../engine/recommendationEngine";
import { RagaEntry } from "../data/ragaKnowledgeBase";

interface Props {
  features: ExtractedFeatures;
  raga: RagaEntry;
}

export default function FeatureRadar({ features, raga }: Props) {
  const patientFeatures = [
    { label: "Stress", value: features.stress_score, color: "#EF4444" },
    { label: "Sleep Disruption", value: features.sleep_disruption, color: "#8B5CF6" },
    { label: "Mood", value: features.mood_score, color: "#3B82F6" },
    { label: "Relaxation Need", value: features.relaxation_need, color: "#10B981" },
    { label: "Emotional Need", value: features.emotional_stability_need, color: "#F59E0B" },
    { label: "Focus Need", value: features.focus_need, color: "#06B6D4" },
    { label: "Pain Level", value: features.pain_level, color: "#EC4899" },
    { label: "Energy", value: features.energy_level, color: "#84CC16" },
  ];

  const ragaFeatures = [
    { label: "Stress Reduction", value: raga.stress_reduction, color: "#EF4444" },
    { label: "Sleep Induction", value: raga.sleep_induction, color: "#8B5CF6" },
    { label: "Depression Help", value: raga.depression_help, color: "#3B82F6" },
    { label: "Stress Reduction", value: raga.stress_reduction, color: "#10B981" },
    { label: "Emotional Stability", value: raga.emotional_stability, color: "#F59E0B" },
    { label: "Focus Enhancement", value: raga.focus_enhancement, color: "#06B6D4" },
    { label: "Pain Relief", value: raga.pain_relief, color: "#EC4899" },
    { label: "Immune Boost", value: raga.immune_boost, color: "#84CC16" },
  ];

  const metrics = [
    { label: "Stress", patientKey: "stress_score", ragaKey: "stress_reduction" as const },
    { label: "Sleep", patientKey: "sleep_disruption", ragaKey: "sleep_induction" as const },
    { label: "Mood/Dep.", patientKey: "mood_score", ragaKey: "depression_help" as const },
    { label: "Relaxation", patientKey: "relaxation_need", ragaKey: "stress_reduction" as const },
    { label: "Emo. Stability", patientKey: "emotional_stability_need", ragaKey: "emotional_stability" as const },
    { label: "Focus", patientKey: "focus_need", ragaKey: "focus_enhancement" as const },
  ];

  // Scoring bounds for reference
  const _maxRagaScore = Math.max(...metrics.map((m) => raga[m.ragaKey] as number), 0.3);
  const _maxPatientScore = Math.max(...metrics.map((m) => features[m.patientKey as keyof ExtractedFeatures] as number), 0.3);
  void _maxRagaScore;
  void _maxPatientScore;

  return (
    <div className="rounded-2xl bg-white p-6 shadow-md">
      <h3 className="mb-4 flex items-center gap-2 text-lg font-semibold text-gray-800">
        <span>📊</span> Patient-Raga Feature Comparison
      </h3>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
        {/* Patient Feature Chart */}
        <div>
          <h4 className="mb-3 text-sm font-semibold text-gray-600">
            👤 Patient Profile
          </h4>
          <div className="space-y-2">
            {patientFeatures.map((f) => (
              <div key={f.label} className="flex items-center gap-2">
                <span className="w-28 text-xs text-gray-500">{f.label}</span>
                <div className="flex-1 h-3 rounded-full bg-gray-100 overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-700"
                    style={{
                      width: `${Math.round(f.value * 100)}%`,
                      backgroundColor: f.color,
                    }}
                  />
                </div>
                <span className="w-10 text-right text-xs font-medium text-gray-700">
                  {Math.round(f.value * 100)}%
                </span>
              </div>
            ))}
          </div>
          <div className="mt-3 flex flex-wrap gap-2 text-xs text-gray-400">
            <span>Arousal pref: <strong className="text-gray-600">{features.arousal_preference}</strong></span>
            <span>Valence pref: <strong className="text-gray-600">{features.valence_preference}</strong></span>
          </div>
        </div>

        {/* Raga Feature Chart */}
        <div>
          <h4 className="mb-3 text-sm font-semibold text-gray-600">
            🎵 {raga.raga_name} Profile
          </h4>
          <div className="space-y-2">
            {ragaFeatures.map((f) => (
              <div key={f.label} className="flex items-center gap-2">
                <span className="w-28 text-xs text-gray-500">{f.label}</span>
                <div className="flex-1 h-3 rounded-full bg-gray-100 overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-700"
                    style={{
                      width: `${Math.round(f.value * 100)}%`,
                      backgroundColor: f.color,
                    }}
                  />
                </div>
                <span className="w-10 text-right text-xs font-medium text-gray-700">
                  {Math.round(f.value * 100)}%
                </span>
              </div>
            ))}
          </div>
          <div className="mt-3 flex flex-wrap gap-2 text-xs text-gray-400">
            <span>Arousal: <strong className="text-gray-600">{(raga.arousal_level * 100).toFixed(0)}%</strong></span>
            <span>Valence: <strong className="text-gray-600">{(raga.valence * 100).toFixed(0)}%</strong></span>
          </div>
        </div>
      </div>

      {/* Match Summary */}
      <div className="mt-6 rounded-xl bg-amber-50 p-4">
        <h4 className="mb-2 text-sm font-semibold text-amber-800">📈 Therapeutic Match Analysis</h4>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
          {metrics.map((m) => {
            const patientVal = features[m.patientKey as keyof ExtractedFeatures] as number;
            const ragaVal = raga[m.ragaKey] as number;
            const matchPct = patientVal > 0 ? Math.min(Math.round((ragaVal / Math.max(patientVal, 0.1)) * 100), 100) : Math.round(ragaVal * 100);
            return (
              <div key={m.label} className="text-center">
                <p className="text-xs text-amber-600">{m.label}</p>
                <p className="text-lg font-bold text-amber-800">{matchPct}%</p>
                <p className="text-[10px] text-amber-500">match</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
