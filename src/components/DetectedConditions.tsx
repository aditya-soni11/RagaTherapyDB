interface Props {
  conditions: string[];
  conditionScores: { condition: string; score: number }[];
}

export default function DetectedConditions({ conditions, conditionScores }: Props) {
  if (conditions.length === 0) return null;

  return (
    <div className="rounded-2xl bg-white p-6 shadow-md">
      <h3 className="mb-3 flex items-center gap-2 text-lg font-semibold text-gray-800">
        <span>🔍</span> NLP Analysis — Detected Conditions
      </h3>

      <div className="flex flex-wrap gap-3">
        {conditionScores.slice(0, 6).map((cs) => {
          const pct = Math.round(cs.score * 100);
          const isTop = cs.condition === conditions[0];
          return (
            <div
              key={cs.condition}
              className={`rounded-xl px-4 py-2 transition-all ${
                isTop
                  ? "bg-amber-100 border border-amber-300 shadow-sm"
                  : "bg-gray-50 border border-gray-100"
              }`}
            >
              <span className="text-sm font-medium text-gray-800 capitalize">
                {cs.condition}
              </span>
              <span className={`ml-2 text-xs font-bold ${isTop ? "text-amber-700" : "text-gray-500"}`}>
                {pct}%
              </span>
            </div>
          );
        })}
      </div>

      <p className="mt-3 text-xs text-gray-400">
        Primary detected: <span className="font-medium text-gray-600 capitalize">{conditions[0]}</span>
        {conditions.length > 1 && (
          <span>, with secondary: {conditions.slice(1).join(", ")}</span>
        )}
      </p>
    </div>
  );
}
