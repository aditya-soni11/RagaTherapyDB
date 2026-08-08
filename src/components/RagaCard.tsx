import { RagaRecommendation } from "../engine/recommendationEngine";

interface Props {
  recommendation: RagaRecommendation;
}

export default function RagaCard({ recommendation }: Props) {
  const { raga, confidence, factorScores } = recommendation;

  const confidenceColor =
    confidence >= 90 ? "text-emerald-600" : confidence >= 75 ? "text-amber-600" : "text-orange-600";
  const confidenceBg =
    confidence >= 90 ? "bg-emerald-100" : confidence >= 75 ? "bg-amber-100" : "bg-orange-100";

  return (
    <div className="overflow-hidden rounded-2xl bg-white shadow-lg shadow-amber-100/50">
      {/* Top bar with color */}
      <div
        className="h-2"
        style={{
          background: `linear-gradient(90deg, ${getMoodColor(raga.mood_color)}, ${getMoodColorAlt(raga.mood_color)})`,
        }}
      />

      <div className="p-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          {/* Raga Name & Details */}
          <div className="flex-1">
            <div className="mb-1 flex items-center gap-3">
              <span className="text-2xl">🎵</span>
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{raga.raga_name}</h2>
                <p className="text-sm text-gray-500">also known as {raga.also_known_as}</p>
              </div>
            </div>

            <div className="mt-3 flex flex-wrap gap-2">
              <Badge icon="🕐" text={raga.time_of_day} />
              <Badge icon="🎼" text={raga.thaat} />
              <Badge icon="💫" text={raga.primary_emotion} />
              <Badge icon="⚡" text={`${raga.tempo_bpm} BPM`} />
              <Badge icon="🎯" text={raga.scale_type} />
            </div>
          </div>

          {/* Confidence Score */}
          <div className="flex flex-col items-center justify-center">
            <div className={`flex h-24 w-24 items-center justify-center rounded-full ${confidenceBg}`}>
              <div className="text-center">
                <span className={`text-2xl font-bold ${confidenceColor}`}>{confidence}%</span>
                <p className="text-[10px] text-gray-500">Confidence</p>
              </div>
            </div>
          </div>
        </div>

        {/* Description */}
        <p className="mt-4 text-sm text-gray-600 leading-relaxed">{raga.brief_description}</p>

        {/* Musical Features */}
        <div className="mt-4 grid grid-cols-2 gap-3 rounded-xl bg-gray-50 p-4 sm:grid-cols-4">
          <MiniStat label="Notes" value={raga.musical_features.notes} />
          <MiniStat label="Vadi" value={raga.musical_features.vadi} />
          <MiniStat label="Samvadi" value={raga.musical_features.samvadi} />
          <MiniStat label="Movement" value={raga.musical_features.movement} />
        </div>

        {/* Factor Scores */}
        <div className="mt-4">
          <h4 className="mb-2 text-sm font-semibold text-gray-700">Factor Scores</h4>
          <div className="space-y-1.5">
            <FactorBar label="Relaxation Profile" score={factorScores.relaxation_profile} />
            <FactorBar label="Emotional Stabilization" score={factorScores.emotional_stabilization} />
            <FactorBar label="Therapy Evidence" score={factorScores.therapy_evidence} />
            <FactorBar label="Acoustic Match" score={factorScores.acoustic_match} />
            <FactorBar label="Similarity Score" score={factorScores.similarity_score} />
          </div>
        </div>

        {/* Target Conditions */}
        <div className="mt-4">
          <h4 className="mb-2 text-sm font-semibold text-gray-700">Therapeutic Targets</h4>
          <div className="flex flex-wrap gap-1.5">
            {raga.target_conditions.map((c) => (
              <span key={c} className="rounded-full bg-amber-50 px-2.5 py-0.5 text-xs text-amber-700">
                {c}
              </span>
            ))}
          </div>
        </div>

        {/* Chakra & Mood */}
        <div className="mt-4 flex flex-wrap gap-4 text-xs text-gray-500">
          <span>
            🎨 Mood: <strong>{raga.mood_color}</strong>
          </span>
          <span>
            🔮 Chakra: <strong>{raga.chakra}</strong>
          </span>
          <span>
            📚 Citations: <strong>{raga.research_citations}</strong>
          </span>
        </div>
      </div>
    </div>
  );
}

function Badge({ icon, text }: { icon: string; text: string }) {
  return (
    <span className="inline-flex items-center gap-1 rounded-full bg-gray-100 px-2.5 py-0.5 text-xs text-gray-600">
      <span>{icon}</span>
      {text}
    </span>
  );
}

function MiniStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="text-center">
      <p className="text-[10px] font-medium text-gray-400 uppercase">{label}</p>
      <p className="text-xs font-semibold text-gray-800">{value}</p>
    </div>
  );
}

function FactorBar({ label, score }: { label: string; score: number }) {
  const pct = Math.round(score * 100);
  const color = pct >= 80 ? "bg-emerald-500" : pct >= 60 ? "bg-amber-500" : "bg-orange-400";
  return (
    <div className="flex items-center gap-2">
      <span className="w-40 text-xs text-gray-600">{label}</span>
      <div className="flex-1 h-2 rounded-full bg-gray-200 overflow-hidden">
        <div className={`h-full rounded-full ${color} transition-all duration-700`} style={{ width: `${pct}%` }} />
      </div>
      <span className="w-10 text-right text-xs font-medium text-gray-700">{pct}%</span>
    </div>
  );
}

function getMoodColor(name: string): string {
  const map: Record<string, string> = {
    Golden: "#F59E0B",
    "Deep Blue": "#1E3A5F",
    "Soft White": "#F8FAFC",
    "Midnight Blue": "#0F172A",
    "Sunrise Orange": "#EA580C",
    Teal: "#0D9488",
    "Spring Green": "#22C55E",
    "Bright Yellow": "#EAB308",
    Violet: "#8B5CF6",
    Saffron: "#F97316",
    "Pale Gold": "#FDE68A",
    "Pearl White": "#F8FAFC",
    "Midnight Black": "#171717",
    Indigo: "#4F46E5",
    Aqua: "#06B6D4",
    "Dusk Purple": "#7C3AED",
    "Pre-dawn Grey": "#6B7280",
    "Moonlight Silver": "#94A3B8",
  };
  return map[name] || "#F59E0B";
}

function getMoodColorAlt(name: string): string {
  const map: Record<string, string> = {
    Golden: "#D97706",
    "Deep Blue": "#2563EB",
    "Soft White": "#E2E8F0",
    "Midnight Blue": "#1E3A5F",
    "Sunrise Orange": "#DC2626",
  };
  return map[name] || "#D97706";
}
