interface Props {
  factors: string[];
}

const FACTOR_ICONS: Record<string, string> = {
  "Relaxation profile": "🧘",
  "Emotional stabilization": "💙",
  "Positive therapy evidence": "📊",
  "Low-arousal acoustic characteristics": "🔉",
  "Similarity to historical recommendations": "📜",
  "Sleep enhancement potential": "😴",
  "Pain relief characteristics": "💊",
  "Focus enhancement properties": "🎯",
  "High stress reduction capability": "🌿",
  "Spiritual uplift potential": "✨",
  "Immune system support": "🛡️",
  "Blood pressure modulation": "❤️",
};

export default function SupportingFactors({ factors }: Props) {
  return (
    <div className="rounded-2xl bg-white p-6 shadow-md">
      <h3 className="mb-4 flex items-center gap-2 text-lg font-semibold text-gray-800">
        <span>✅</span> Supporting Factors
      </h3>
      <div className="space-y-3">
        {factors.map((factor, i) => (
          <div
            key={i}
            className="flex items-start gap-3 rounded-lg bg-green-50 p-3 transition-all hover:bg-green-100"
          >
            <span className="mt-0.5 text-lg">{FACTOR_ICONS[factor] || "✔️"}</span>
            <div>
              <p className="text-sm font-medium text-gray-800">{factor}</p>
            </div>
          </div>
        ))}
      </div>
      {factors.length === 0 && (
        <p className="text-sm text-gray-400">No specific supporting factors identified.</p>
      )}
    </div>
  );
}
