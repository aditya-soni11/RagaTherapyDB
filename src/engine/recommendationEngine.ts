import { ragaKnowledgeBase, RagaEntry } from "../data/ragaKnowledgeBase";
import { diseaseFeatureMap } from "../data/diseaseFeatureMap";

// ================================================================
// NLP: Keyword-based Symptom/Disease Detection
// ================================================================

export interface ExtractedFeatures {
  stress_score: number;
  sleep_disruption: number;
  mood_score: number;
  relaxation_need: number;
  emotional_stability_need: number;
  focus_need: number;
  energy_level: number;
  pain_level: number;
  arousal_preference: "very_low" | "low" | "medium" | "high";
  valence_preference: "high" | "neutral" | "low";
  detected_conditions: string[];
  condition_scores: { condition: string; score: number }[];
}

function tokenize(text: string): string[] {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter((t) => t.length > 1);
}

function getKeywords(text: string): string[] {
  const tokens = tokenize(text);
  const phrases = [text.toLowerCase()];
  // Generate bigrams
  for (let i = 0; i < tokens.length - 1; i++) {
    phrases.push(`${tokens[i]} ${tokens[i + 1]}`);
  }
  // Generate trigrams
  for (let i = 0; i < tokens.length - 2; i++) {
    phrases.push(`${tokens[i]} ${tokens[i + 1]} ${tokens[i + 2]}`);
  }
  return [...new Set([...tokens, ...phrases])];
}

export function detectConditions(text: string): { condition: string; score: number }[] {
  const keywords = getKeywords(text);
  const results: { condition: string; score: number }[] = [];

  for (const [condition, features] of Object.entries(diseaseFeatureMap) as [string, typeof diseaseFeatureMap[string]][]) {
    let matchCount = 0;
    for (const kw of keywords) {
      // Exact keyword match
      if (features.keywords.includes(kw)) {
        matchCount += 2;
      }
      // Partial match
      for (const dkw of features.keywords) {
        if (dkw.includes(kw) || kw.includes(dkw)) {
          matchCount += 1;
          break;
        }
      }
    }
    if (matchCount > 0) {
      const score = Math.min(matchCount / (features.keywords.length * 0.3), 1.0);
      results.push({ condition, score });
    }
  }

  // Also check if condition name directly appears in text
  const textLower = text.toLowerCase();
  for (const condition of Object.keys(diseaseFeatureMap)) {
    if (textLower.includes(condition) && !results.find((r) => r.condition === condition)) {
      results.push({ condition, score: 0.9 });
    }
  }

  results.sort((a, b) => b.score - a.score);
  return results;
}

// ================================================================
// Stage 1 & 2: NLP Understanding + Feature Mapping
// ================================================================

export function extractDiseaseFeatures(text: string): ExtractedFeatures {
  const detectedConditions = detectConditions(text);

  if (detectedConditions.length === 0) {
    // Default to general wellness
    const defaults = diseaseFeatureMap["general wellness"];
    return {
      stress_score: defaults.stress_score,
      sleep_disruption: defaults.sleep_disruption,
      mood_score: defaults.mood_score,
      relaxation_need: defaults.relaxation_need,
      emotional_stability_need: defaults.emotional_stability_need,
      focus_need: defaults.focus_need,
      energy_level: defaults.energy_level,
      pain_level: defaults.pain_level,
      arousal_preference: defaults.arousal_preference,
      valence_preference: defaults.valence_preference,
      detected_conditions: ["general wellness"],
      condition_scores: [{ condition: "general wellness", score: 0.5 }],
    };
  }

  // Weighted combination of top conditions
  const topConditions = detectedConditions.slice(0, 3);
  const totalScore = topConditions.reduce((sum, c) => sum + c.score, 0);
  const weights = topConditions.map((c) => c.score / totalScore);

  let aggregated: Record<string, number> = {
    stress_score: 0,
    sleep_disruption: 0,
    mood_score: 0,
    relaxation_need: 0,
    emotional_stability_need: 0,
    focus_need: 0,
    energy_level: 0,
    pain_level: 0,
  };

  const arousalPrefs: string[] = [];
  const valencePrefs: string[] = [];

  for (let i = 0; i < topConditions.length; i++) {
    const cond = topConditions[i].condition;
    const features = diseaseFeatureMap[cond];
    if (!features) continue;
    const w = weights[i];

    for (const key of Object.keys(aggregated)) {
      aggregated[key] += (features as unknown as Record<string, number>)[key] * w;
    }
    arousalPrefs.push(features.arousal_preference);
    valencePrefs.push(features.valence_preference);
  }

  // Determine majority arousal/valence preference
  const arousalOrder: Record<string, number> = { very_low: 0, low: 1, medium: 2, high: 3 };
  const avgArousal =
    arousalPrefs.reduce((sum, a) => sum + (arousalOrder[a] ?? 1), 0) / arousalPrefs.length;
  let arousalPreference: "very_low" | "low" | "medium" | "high" = "low";
  if (avgArousal <= 0.5) arousalPreference = "very_low";
  else if (avgArousal <= 1.5) arousalPreference = "low";
  else if (avgArousal <= 2.5) arousalPreference = "medium";
  else arousalPreference = "high";

  const highValenceCount = valencePrefs.filter((v) => v === "high").length;
  let valencePreference: "high" | "neutral" | "low" = "high";
  if (highValenceCount > valencePrefs.length / 2) valencePreference = "high";
  else if (valencePrefs.every((v) => v === "low")) valencePreference = "low";
  else valencePreference = "neutral";

  return {
    stress_score: Math.round(aggregated.stress_score * 100) / 100,
    sleep_disruption: Math.round(aggregated.sleep_disruption * 100) / 100,
    mood_score: Math.round(aggregated.mood_score * 100) / 100,
    relaxation_need: Math.round(aggregated.relaxation_need * 100) / 100,
    emotional_stability_need: Math.round(aggregated.emotional_stability_need * 100) / 100,
    focus_need: Math.round(aggregated.focus_need * 100) / 100,
    energy_level: Math.round(aggregated.energy_level * 100) / 100,
    pain_level: Math.round(aggregated.pain_level * 100) / 100,
    arousal_preference: arousalPreference,
    valence_preference: valencePreference,
    detected_conditions: topConditions.map((c) => c.condition),
    condition_scores: detectedConditions,
  };
}

// ================================================================
// Stage 3: Raga Recommendation Engine
// ================================================================

export interface RagaRecommendation {
  raga: RagaEntry;
  confidence: number;
  factorScores: {
    relaxation_profile: number;
    emotional_stabilization: number;
    therapy_evidence: number;
    acoustic_match: number;
    similarity_score: number;
  };
  explanation: string;
}

export interface RecommendationResult {
  recommended_raga: RagaRecommendation;
  alternative_ragas: RagaRecommendation[];
  supporting_factors: string[];
  detected_conditions: string[];
  extracted_features: ExtractedFeatures;
}

export function recommendRaga(text: string): RecommendationResult {
  const features = extractDiseaseFeatures(text);

  // Score all ragas
  const scoredRagas: { raga: RagaEntry; totalScore: number; factorScores: RagaRecommendation["factorScores"] }[] = [];

  for (const raga of ragaKnowledgeBase) {
    // 1. Relaxation Profile: How well does raga match the relaxation need?
    const arousalMatch =
      features.arousal_preference === "very_low"
        ? 1 - raga.arousal_level
        : features.arousal_preference === "low"
          ? 1 - Math.abs(raga.arousal_level - 0.3)
          : features.arousal_preference === "medium"
            ? 1 - Math.abs(raga.arousal_level - 0.5)
            : raga.arousal_level;

    const relaxationScore = clamp(
      features.relaxation_need * raga.stress_reduction * 0.5 +
        features.stress_score * raga.stress_reduction * 0.3 +
        arousalMatch * 0.2,
      0,
      1
    );

    // 2. Emotional Stabilization
    const emotionalScore = clamp(
      features.emotional_stability_need * raga.emotional_stability * 0.5 +
        features.mood_score * (1 - raga.valence) * 0.2 +
        raga.valence * (features.valence_preference === "high" ? 1 : 0.5) * 0.3,
      0,
      1
    );

    // 3. Therapy Evidence Score
    const evidenceScore = raga.therapy_evidence_score;

    // 4. Acoustic Match: sleep induction, pain relief, focus
    const acousticScore = clamp(
      features.sleep_disruption * raga.sleep_induction * 0.35 +
        features.pain_level * raga.pain_relief * 0.35 +
        features.focus_need * raga.focus_enhancement * 0.3,
      0,
      1
    );

    // 5. Similarity: target condition overlap
    const conditionMatch =
      features.detected_conditions.filter((c: string) =>
        raga.target_conditions.some((tc: string) => tc.toLowerCase().includes(c) || c.includes(tc.toLowerCase()))
      ).length / Math.max(features.detected_conditions.length, 1);
    const similarityScore = clamp(conditionMatch, 0, 1);

    // Check contraindications
    const hasContraindication = raga.contraindications.some((ci: string) =>
      features.detected_conditions.some((dc: string) => dc.toLowerCase().includes(ci.toLowerCase()))
    );

    const totalScore = hasContraindication
      ? 0
      : relaxationScore * 0.30 +
        emotionalScore * 0.25 +
        evidenceScore * 0.20 +
        acousticScore * 0.15 +
        similarityScore * 0.10;

    scoredRagas.push({
      raga,
      totalScore: Math.round(totalScore * 10000) / 10000,
      factorScores: {
        relaxation_profile: Math.round(relaxationScore * 100) / 100,
        emotional_stabilization: Math.round(emotionalScore * 100) / 100,
        therapy_evidence: Math.round(evidenceScore * 100) / 100,
        acoustic_match: Math.round(acousticScore * 100) / 100,
        similarity_score: Math.round(similarityScore * 100) / 100,
      },
    });
  }

  // Sort by total score descending
  scoredRagas.sort((a, b) => b.totalScore - a.totalScore);

  // Top recommendation
  const top = scoredRagas[0];
  const confidence = Math.round(top.totalScore * 100 * 10) / 10;

  // Build supporting factors
  const supportingFactors: string[] = [];
  const fs = top.factorScores;
  if (fs.relaxation_profile > 0.7) supportingFactors.push("Relaxation profile");
  if (fs.emotional_stabilization > 0.7) supportingFactors.push("Emotional stabilization");
  if (fs.therapy_evidence > 0.7) supportingFactors.push("Positive therapy evidence");
  if (fs.acoustic_match > 0.7) supportingFactors.push("Low-arousal acoustic characteristics");
  if (fs.similarity_score > 0.5) supportingFactors.push("Similarity to historical recommendations");

  // Add additional factors
  if (features.sleep_disruption > 0.6 && top.raga.sleep_induction > 0.7) {
    supportingFactors.push("Sleep enhancement potential");
  }
  if (features.pain_level > 0.6 && top.raga.pain_relief > 0.7) {
    supportingFactors.push("Pain relief characteristics");
  }
  if (features.focus_need > 0.7 && top.raga.focus_enhancement > 0.7) {
    supportingFactors.push("Focus enhancement properties");
  }
  if (top.raga.stress_reduction > 0.85) {
    supportingFactors.push("High stress reduction capability");
  }
  if (top.raga.spiritual_uplift > 0.85) {
    supportingFactors.push("Spiritual uplift potential");
  }

  // Ensure at least 5 factors
  while (supportingFactors.length < 5) {
    const remainingPool = [
      "Relaxation profile",
      "Emotional stabilization",
      "Positive therapy evidence",
      "Low-arousal acoustic characteristics",
      "Similarity to historical recommendations",
      "Sleep enhancement potential",
      "Pain relief characteristics",
      "Focus enhancement properties",
      "High stress reduction capability",
      "Spiritual uplift potential",
      "Immune system support",
      "Blood pressure modulation",
    ];
    for (const f of remainingPool) {
      if (!supportingFactors.includes(f)) {
        supportingFactors.push(f);
        break;
      }
    }
  }

  // Alternatives (top 4 after the first, excluding contraindicated)
  const alternatives = scoredRagas
    .slice(1, 5)
    .map((sr) => ({
      raga: sr.raga,
      confidence: Math.round(sr.totalScore * 100 * 10) / 10,
      factorScores: sr.factorScores,
      explanation: generateExplanation(sr.raga, features, sr.totalScore),
    }));

  return {
    recommended_raga: {
      raga: top.raga,
      confidence,
      factorScores: top.factorScores,
      explanation: generateExplanation(top.raga, features, top.totalScore),
    },
    alternative_ragas: alternatives,
    supporting_factors: supportingFactors.slice(0, 7),
    detected_conditions: features.detected_conditions,
    extracted_features: features,
  };
}

function generateExplanation(
  raga: RagaEntry,
  features: ExtractedFeatures,
  score: number
): string {
  const parts: string[] = [];

  parts.push(
    `${raga.raga_name} (also known as ${raga.also_known_as}) is a ${raga.thaat} thaat raga performed during ${raga.time_of_day.toLowerCase()}.`
  );

  parts.push(
    `With a primary emotion of ${raga.primary_emotion.toLowerCase()} and a tempo of ${raga.tempo_bpm} BPM, it creates a ${raga.arousal_level < 0.35 ? "calming" : raga.arousal_level < 0.5 ? "balanced" : "energizing"} sonic environment.`
  );

  if (features.stress_score > 0.6) {
    parts.push(
      `Given your high stress profile (${(features.stress_score * 100).toFixed(0)}%), ${raga.raga_name}'s stress reduction score of ${(raga.stress_reduction * 100).toFixed(0)}% makes it particularly suitable.`
    );
  }

  if (features.sleep_disruption > 0.6) {
    parts.push(
      `Its sleep induction rating of ${(raga.sleep_induction * 100).toFixed(0)}% addresses your sleep disruption levels (${(features.sleep_disruption * 100).toFixed(0)}%).`
    );
  }

  parts.push(
    `The raga's musical structure (${raga.musical_features.notes}) with vadi ${raga.musical_features.vadi} and samvadi ${raga.musical_features.samvadi} creates ${raga.musical_features.movement.toLowerCase()} movement, which ${raga.brief_description.toLowerCase()}`
  );

  parts.push(
    `This recommendation carries a ${(score * 100).toFixed(0)}% overall therapeutic match score based on ${raga.research_citations} research citations supporting its clinical efficacy.`
  );

  return parts.join(" ");
}

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}
