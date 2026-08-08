import { RagaRecommendation } from "../engine/recommendationEngine";

interface Props {
  alternatives: RagaRecommendation[];
}

export default function AlternativeRagas({ alternatives }: Props) {
  if (alternatives.length === 0) return null;

  return (
    <div className="rounded-2xl bg-white p-6 shadow-md">
      <h3 className="mb-4 flex items-center gap-2 text-lg font-semibold text-gray-800">
        <span>🔄</span> Alternative Ragas
      </h3>
      <p className="mb-4 text-sm text-gray-500">
        These ragas scored highly on therapeutic match and may also be suitable for your condition:
      </p>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {alternatives.map((alt, i) => (
          <div
            key={i}
            className="rounded-xl border border-gray-100 bg-gray-50 p-4 transition-all hover:border-amber-200 hover:shadow-md"
          >
            <div className="mb-2 flex items-center justify-between">
              <h4 className="font-semibold text-gray-800">{alt.raga.raga_name}</h4>
              <span className="rounded-full bg-amber-100 px-2 py-0.5 text-xs font-medium text-amber-700">
                {alt.confidence}%
              </span>
            </div>
            <p className="text-xs text-gray-500 mb-1">
              {alt.raga.primary_emotion} • {alt.raga.time_of_day}
            </p>
            <p className="text-xs text-gray-400 line-clamp-2">{alt.raga.brief_description}</p>
            <div className="mt-2 flex flex-wrap gap-1">
              {alt.raga.target_conditions.slice(0, 2).map((c) => (
                <span key={c} className="rounded-full bg-white px-1.5 py-0.5 text-[10px] text-gray-500">
                  {c}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
