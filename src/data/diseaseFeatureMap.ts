export interface DiseaseFeatures {
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
  keywords: string[];
}

export const diseaseFeatureMap: Record<string, DiseaseFeatures> = {
  anxiety: {
    stress_score: 0.85,
    sleep_disruption: 0.80,
    mood_score: 0.25,
    relaxation_need: 0.90,
    emotional_stability_need: 0.88,
    focus_need: 0.70,
    energy_level: 0.30,
    pain_level: 0.40,
    arousal_preference: "low",
    valence_preference: "high",
    keywords: [
      "anxiety", "anxious", "worry", "nervous", "fear", "panic",
      "stress", "restless", "tense", "uneasy", "apprehensive",
      "dread", "nervousness", "agitation"
    ],
  },
  depression: {
    stress_score: 0.70,
    sleep_disruption: 0.85,
    mood_score: 0.15,
    relaxation_need: 0.85,
    emotional_stability_need: 0.90,
    focus_need: 0.65,
    energy_level: 0.20,
    pain_level: 0.50,
    arousal_preference: "medium",
    valence_preference: "high",
    keywords: [
      "depression", "depressed", "sad", "hopeless", "worthless",
      "empty", "low mood", "grief", "melancholy", "unhappy",
      "miserable", "down", "blue", "despair", "crying"
    ],
  },
  insomnia: {
    stress_score: 0.60,
    sleep_disruption: 0.95,
    mood_score: 0.45,
    relaxation_need: 0.90,
    emotional_stability_need: 0.75,
    focus_need: 0.60,
    energy_level: 0.30,
    pain_level: 0.30,
    arousal_preference: "very_low",
    valence_preference: "neutral",
    keywords: [
      "insomnia", "sleepless", "can't sleep", "sleep problem",
      "sleep disorder", "awake", "night", "tired", "sleep",
      "unable to sleep", "wakeful", "restless night"
    ],
  },
  stress: {
    stress_score: 0.95,
    sleep_disruption: 0.78,
    mood_score: 0.30,
    relaxation_need: 0.95,
    emotional_stability_need: 0.80,
    focus_need: 0.75,
    energy_level: 0.45,
    pain_level: 0.50,
    arousal_preference: "low",
    valence_preference: "high",
    keywords: [
      "stress", "stressed", "pressure", "overwhelmed", "burden",
      "tension", "strain", "work stress", "overworked", "burnout",
      "exhausted", "fried", "high stress", "stress levels"
    ],
  },
  hypertension: {
    stress_score: 0.88,
    sleep_disruption: 0.70,
    mood_score: 0.40,
    relaxation_need: 0.88,
    emotional_stability_need: 0.75,
    focus_need: 0.65,
    energy_level: 0.50,
    pain_level: 0.65,
    arousal_preference: "low",
    valence_preference: "neutral",
    keywords: [
      "hypertension", "high blood pressure", "bp", "blood pressure",
      "cardiovascular", "heart", "palpitation"
    ],
  },
  ptsd: {
    stress_score: 0.90,
    sleep_disruption: 0.88,
    mood_score: 0.20,
    relaxation_need: 0.92,
    emotional_stability_need: 0.95,
    focus_need: 0.68,
    energy_level: 0.25,
    pain_level: 0.60,
    arousal_preference: "very_low",
    valence_preference: "high",
    keywords: [
      "ptsd", "trauma", "traumatic", "flashback", "nightmare",
      "trigger", "war", "abuse", "post traumatic"
    ],
  },
  adhd: {
    stress_score: 0.72,
    sleep_disruption: 0.65,
    mood_score: 0.40,
    relaxation_need: 0.75,
    emotional_stability_need: 0.82,
    focus_need: 0.90,
    energy_level: 0.55,
    pain_level: 0.30,
    arousal_preference: "low",
    valence_preference: "high",
    keywords: [
      "adhd", "attention", "focus", "concentrate", "hyperactive",
      "distracted", "add", "attention deficit"
    ],
  },
  ocd: {
    stress_score: 0.80,
    sleep_disruption: 0.75,
    mood_score: 0.35,
    relaxation_need: 0.85,
    emotional_stability_need: 0.88,
    focus_need: 0.80,
    energy_level: 0.45,
    pain_level: 0.45,
    arousal_preference: "low",
    valence_preference: "neutral",
    keywords: [
      "ocd", "obsessive", "compulsive", "intrusive thoughts",
      "rituals", "repetitive", "obsession"
    ],
  },
  "panic disorder": {
    stress_score: 0.88,
    sleep_disruption: 0.82,
    mood_score: 0.22,
    relaxation_need: 0.90,
    emotional_stability_need: 0.90,
    focus_need: 0.65,
    energy_level: 0.28,
    pain_level: 0.55,
    arousal_preference: "very_low",
    valence_preference: "high",
    keywords: [
      "panic", "panic attack", "heart racing", "chest tight",
      "breathless", "dizzy", "fear", "palpitations", "racing heart"
    ],
  },
  "chronic pain": {
    stress_score: 0.75,
    sleep_disruption: 0.78,
    mood_score: 0.35,
    relaxation_need: 0.85,
    emotional_stability_need: 0.80,
    focus_need: 0.65,
    energy_level: 0.35,
    pain_level: 0.85,
    arousal_preference: "very_low",
    valence_preference: "neutral",
    keywords: [
      "pain", "chronic pain", "ache", "hurt", "fibromyalgia",
      "arthritis", "back pain", "sore", "aching"
    ],
  },
  migraine: {
    stress_score: 0.80,
    sleep_disruption: 0.85,
    mood_score: 0.38,
    relaxation_need: 0.82,
    emotional_stability_need: 0.72,
    focus_need: 0.60,
    energy_level: 0.40,
    pain_level: 0.80,
    arousal_preference: "very_low",
    valence_preference: "neutral",
    keywords: [
      "migraine", "headache", "throbbing", "head pain", "nausea",
      "light sensitive", "migraine attack"
    ],
  },
  "chronic fatigue": {
    stress_score: 0.65,
    sleep_disruption: 0.72,
    mood_score: 0.35,
    relaxation_need: 0.80,
    emotional_stability_need: 0.75,
    focus_need: 0.68,
    energy_level: 0.15,
    pain_level: 0.55,
    arousal_preference: "medium",
    valence_preference: "high",
    keywords: [
      "fatigue", "chronic fatigue", "tiredness", "exhaustion",
      "low energy", "drained", "lethargy", "no energy"
    ],
  },
  "bipolar disorder": {
    stress_score: 0.75,
    sleep_disruption: 0.90,
    mood_score: 0.30,
    relaxation_need: 0.80,
    emotional_stability_need: 0.92,
    focus_need: 0.72,
    energy_level: 0.40,
    pain_level: 0.45,
    arousal_preference: "low",
    valence_preference: "neutral",
    keywords: [
      "bipolar", "manic", "mania", "mood swings", "euphoria",
      "cycle", "mood disorder"
    ],
  },
  "eating disorder": {
    stress_score: 0.78,
    sleep_disruption: 0.72,
    mood_score: 0.25,
    relaxation_need: 0.82,
    emotional_stability_need: 0.88,
    focus_need: 0.68,
    energy_level: 0.35,
    pain_level: 0.50,
    arousal_preference: "low",
    valence_preference: "high",
    keywords: [
      "eating disorder", "anorexia", "bulimia", "binge eating",
      "body image", "food", "weight"
    ],
  },
  addiction: {
    stress_score: 0.82,
    sleep_disruption: 0.80,
    mood_score: 0.30,
    relaxation_need: 0.78,
    emotional_stability_need: 0.85,
    focus_need: 0.72,
    energy_level: 0.40,
    pain_level: 0.45,
    arousal_preference: "medium",
    valence_preference: "high",
    keywords: [
      "addiction", "substance", "alcohol", "drug", "craving",
      "withdrawal", "recovery", "sobriety"
    ],
  },
  "heart disease": {
    stress_score: 0.85,
    sleep_disruption: 0.65,
    mood_score: 0.42,
    relaxation_need: 0.88,
    emotional_stability_need: 0.78,
    focus_need: 0.68,
    energy_level: 0.45,
    pain_level: 0.70,
    arousal_preference: "low",
    valence_preference: "high",
    keywords: [
      "heart disease", "cardiac", "heart attack", "coronary",
      "palpitation", "chest pain", "heart condition"
    ],
  },
  dementia: {
    stress_score: 0.45,
    sleep_disruption: 0.88,
    mood_score: 0.40,
    relaxation_need: 0.65,
    emotional_stability_need: 0.70,
    focus_need: 0.55,
    energy_level: 0.25,
    pain_level: 0.40,
    arousal_preference: "low",
    valence_preference: "high",
    keywords: [
      "dementia", "alzheimer", "memory loss", "cognitive decline",
      "forgetful", "confusion", "memory"
    ],
  },
  autism: {
    stress_score: 0.55,
    sleep_disruption: 0.60,
    mood_score: 0.50,
    relaxation_need: 0.70,
    emotional_stability_need: 0.85,
    focus_need: 0.85,
    energy_level: 0.50,
    pain_level: 0.25,
    arousal_preference: "low",
    valence_preference: "high",
    keywords: [
      "autism", "asd", "spectrum", "sensory", "social",
      "communication", "neurodivergent"
    ],
  },
  ibs: {
    stress_score: 0.72,
    sleep_disruption: 0.68,
    mood_score: 0.40,
    relaxation_need: 0.80,
    emotional_stability_need: 0.72,
    focus_need: 0.62,
    energy_level: 0.45,
    pain_level: 0.70,
    arousal_preference: "low",
    valence_preference: "neutral",
    keywords: [
      "ibs", "irritable bowel", "stomach pain", "digestive",
      "gut", "colon", "constipation", "diarrhea", "bloating"
    ],
  },
  cancer: {
    stress_score: 0.82,
    sleep_disruption: 0.85,
    mood_score: 0.25,
    relaxation_need: 0.85,
    emotional_stability_need: 0.88,
    focus_need: 0.70,
    energy_level: 0.30,
    pain_level: 0.82,
    arousal_preference: "very_low",
    valence_preference: "high",
    keywords: [
      "cancer", "tumor", "chemotherapy", "radiation", "oncology",
      "malignant", "cancer patient"
    ],
  },
  loneliness: {
    stress_score: 0.65,
    sleep_disruption: 0.68,
    mood_score: 0.28,
    relaxation_need: 0.78,
    emotional_stability_need: 0.82,
    focus_need: 0.62,
    energy_level: 0.35,
    pain_level: 0.40,
    arousal_preference: "low",
    valence_preference: "high",
    keywords: [
      "lonely", "loneliness", "alone", "isolated", "isolation",
      "social isolation", "no friends", "disconnected"
    ],
  },
  grief: {
    stress_score: 0.78,
    sleep_disruption: 0.82,
    mood_score: 0.18,
    relaxation_need: 0.82,
    emotional_stability_need: 0.88,
    focus_need: 0.55,
    energy_level: 0.25,
    pain_level: 0.50,
    arousal_preference: "low",
    valence_preference: "neutral",
    keywords: [
      "grief", "loss", "bereavement", "mourning", "death",
      "lost someone", "heartbreak"
    ],
  },
  "general wellness": {
    stress_score: 0.40,
    sleep_disruption: 0.35,
    mood_score: 0.65,
    relaxation_need: 0.60,
    emotional_stability_need: 0.65,
    focus_need: 0.65,
    energy_level: 0.65,
    pain_level: 0.20,
    arousal_preference: "medium",
    valence_preference: "high",
    keywords: [
      "wellness", "relax", "meditation", "calm", "peace",
      "balance", "wellbeing", "harmony", "relaxation"
    ],
  },
};

export default diseaseFeatureMap;
