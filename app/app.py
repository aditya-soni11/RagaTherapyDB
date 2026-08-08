"""
RagaTherapy: AI-Powered Disease-Aware Raga Recommendation System
Streamlit Web Application

Run: streamlit run app/app.py
"""

import streamlit as st
import json
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ================================================================
# PAGE CONFIG
# ================================================================
st.set_page_config(
    page_title="RagaTherapy — AI Raga Recommendation",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ================================================================
# CUSTOM CSS
# ================================================================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #F59E0B, #EA580C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #6B7280;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .raga-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .confidence-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-weight: 700;
        font-size: 1.2rem;
    }
    .factor-item {
        background: #F0FDF4;
        border-radius: 0.5rem;
        padding: 0.75rem;
        margin: 0.25rem 0;
    }
    .alt-raga-card {
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 0.75rem;
        padding: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ================================================================
# LOAD KNOWLEDGE BASE
# ================================================================

@st.cache_resource
def load_knowledge_base():
    """Load or create the raga knowledge base."""
    kb_path = Path("data/knowledge_base/raga_knowledge_base.json")
    disease_path = Path("data/knowledge_base/disease_feature_map.json")

    if kb_path.exists() and disease_path.exists():
        with open(kb_path) as f:
            raga_kb = json.load(f)
        with open(disease_path) as f:
            disease_map = json.load(f)
    else:
        # Embedded fallback
        raga_kb, disease_map = create_embedded_kb()

    return raga_kb, disease_map


def create_embedded_kb():
    """Create knowledge bases from embedded data."""
    # This mirrors the React app's embedded data
    # For brevity, we load a simplified version
    raga_kb = [
        {
            "raga_name": "Yaman", "also_known_as": "Kalyan",
            "time_of_day": "Evening", "thaat": "Kalyan",
            "arousal_level": 0.35, "valence": 0.80, "tempo_bpm": 60,
            "primary_emotion": "Peace", "secondary_emotion": "Joy",
            "stress_reduction": 0.92, "anxiety_relief": 0.90,
            "depression_help": 0.75, "sleep_induction": 0.65,
            "pain_relief": 0.60, "focus_enhancement": 0.72,
            "emotional_stability": 0.88, "blood_pressure_reduction": 0.70,
            "immune_boost": 0.65, "spiritual_uplift": 0.85,
            "therapy_evidence_score": 0.92, "popularity_score": 0.95,
            "research_citations": 47, "frequency_hz": 256,
            "scale_type": "Heptatonic", "mood_color": "Golden",
            "chakra": "Anahata",
            "target_conditions": ["Anxiety", "Stress", "Depression", "Hypertension"],
            "contraindications": ["Manic episodes"],
            "brief_description": "Yaman evokes a serene and sublime atmosphere, effective in reducing cortisol levels.",
            "musical_features": {"notes": "Sa Re Ga Ma# Pa Dha Ni Sa", "vadi": "Ga", "samvadi": "Ni", "movement": "Both ascending and descending"}
        },
        {
            "raga_name": "Darbari Kanada", "also_known_as": "Darbari",
            "time_of_day": "Late Night", "thaat": "Asavari",
            "arousal_level": 0.25, "valence": 0.65, "tempo_bpm": 45,
            "primary_emotion": "Depth", "secondary_emotion": "Serenity",
            "stress_reduction": 0.95, "anxiety_relief": 0.88,
            "depression_help": 0.82, "sleep_induction": 0.90,
            "pain_relief": 0.72, "focus_enhancement": 0.65,
            "emotional_stability": 0.92, "blood_pressure_reduction": 0.85,
            "immune_boost": 0.68, "spiritual_uplift": 0.88,
            "therapy_evidence_score": 0.90, "popularity_score": 0.88,
            "research_citations": 38, "frequency_hz": 240,
            "scale_type": "Heptatonic", "mood_color": "Deep Blue",
            "chakra": "Vishuddha",
            "target_conditions": ["Insomnia", "Hypertension", "Stress", "Anxiety", "PTSD"],
            "contraindications": ["Acute Depression"],
            "brief_description": "Darbari's slow melodic movement reduces cortisol and sympathetic activity.",
            "musical_features": {"notes": "Sa Re Ga♭ Ma Pa Dha♭ Ni♭ Sa", "vadi": "Re", "samvadi": "Pa", "movement": "Slow, deliberate"}
        },
        {
            "raga_name": "Bhairavi", "also_known_as": "Sindhu Bhairavi",
            "time_of_day": "Morning", "thaat": "Bhairavi",
            "arousal_level": 0.30, "valence": 0.70, "tempo_bpm": 55,
            "primary_emotion": "Compassion", "secondary_emotion": "Devotion",
            "stress_reduction": 0.88, "anxiety_relief": 0.85,
            "depression_help": 0.90, "sleep_induction": 0.78,
            "pain_relief": 0.80, "focus_enhancement": 0.70,
            "emotional_stability": 0.90, "blood_pressure_reduction": 0.78,
            "immune_boost": 0.72, "spiritual_uplift": 0.92,
            "therapy_evidence_score": 0.91, "popularity_score": 0.92,
            "research_citations": 52, "frequency_hz": 220,
            "scale_type": "Heptatonic", "mood_color": "Soft White",
            "chakra": "Sahasrara",
            "target_conditions": ["Depression", "Grief", "Emotional Pain", "Anxiety"],
            "contraindications": [],
            "brief_description": "Bhairavi's all-komal notes create a deeply compassionate sonic environment, shown to reduce depressive symptoms.",
            "musical_features": {"notes": "Sa Re♭ Ga♭ Ma Pa Dha♭ Ni♭ Sa", "vadi": "Ma", "samvadi": "Sa", "movement": "Gentle, all-encompassing"}
        },
        {
            "raga_name": "Bageshree", "also_known_as": "Bageshri",
            "time_of_day": "Late Night", "thaat": "Kafi",
            "arousal_level": 0.28, "valence": 0.72, "tempo_bpm": 50,
            "primary_emotion": "Yearning", "secondary_emotion": "Calm",
            "stress_reduction": 0.90, "anxiety_relief": 0.88,
            "depression_help": 0.85, "sleep_induction": 0.92,
            "pain_relief": 0.70, "focus_enhancement": 0.68,
            "emotional_stability": 0.85, "blood_pressure_reduction": 0.80,
            "immune_boost": 0.65, "spiritual_uplift": 0.82,
            "therapy_evidence_score": 0.87, "popularity_score": 0.82,
            "research_citations": 29, "frequency_hz": 228,
            "scale_type": "Heptatonic", "mood_color": "Midnight Blue",
            "chakra": "Ajna",
            "target_conditions": ["Insomnia", "Anxiety", "Chronic Stress", "Loneliness", "PTSD"],
            "contraindications": ["Severe Depression"],
            "brief_description": "Bageshree's late-night character makes it ideal for sleep induction and anxiety management.",
            "musical_features": {"notes": "Sa Re♭ Ga♭ Ma Pa Dha Ni♭ Sa", "vadi": "Ma", "samvadi": "Sa", "movement": "Languid, flowing"}
        },
        {
            "raga_name": "Malkaus", "also_known_as": "Malkauns",
            "time_of_day": "Late Night", "thaat": "Bhairavi",
            "arousal_level": 0.22, "valence": 0.60, "tempo_bpm": 40,
            "primary_emotion": "Deep Calm", "secondary_emotion": "Gravity",
            "stress_reduction": 0.92, "anxiety_relief": 0.88,
            "depression_help": 0.70, "sleep_induction": 0.95,
            "pain_relief": 0.85, "focus_enhancement": 0.60,
            "emotional_stability": 0.88, "blood_pressure_reduction": 0.90,
            "immune_boost": 0.70, "spiritual_uplift": 0.85,
            "therapy_evidence_score": 0.89, "popularity_score": 0.85,
            "research_citations": 35, "frequency_hz": 218,
            "scale_type": "Pentatonic", "mood_color": "Midnight Black",
            "chakra": "Muladhara",
            "target_conditions": ["Severe Insomnia", "Hypertension", "Chronic Pain", "PTSD", "Extreme Stress"],
            "contraindications": ["Depression", "Grief"],
            "brief_description": "Malkaus is the most potent sleep-inducing raga; all-komal pentatonic creates profound parasympathetic activation.",
            "musical_features": {"notes": "Sa Ga♭ Ma Dha♭ Ni♭ Sa", "vadi": "Ma", "samvadi": "Sa", "movement": "Deep, slow, grave"}
        },
        {
            "raga_name": "Bhimpalasi", "also_known_as": "Bhimpalas",
            "time_of_day": "Afternoon", "thaat": "Kafi",
            "arousal_level": 0.35, "valence": 0.72, "tempo_bpm": 55,
            "primary_emotion": "Serenity", "secondary_emotion": "Peace",
            "stress_reduction": 0.88, "anxiety_relief": 0.85,
            "depression_help": 0.80, "sleep_induction": 0.80,
            "pain_relief": 0.78, "focus_enhancement": 0.70,
            "emotional_stability": 0.86, "blood_pressure_reduction": 0.82,
            "immune_boost": 0.70, "spiritual_uplift": 0.82,
            "therapy_evidence_score": 0.85, "popularity_score": 0.82,
            "research_citations": 28, "frequency_hz": 248,
            "scale_type": "Pentatonic", "mood_color": "Aqua",
            "chakra": "Vishuddha",
            "target_conditions": ["Anxiety", "Stress", "Hypertension", "Afternoon Fatigue", "IBS"],
            "contraindications": [],
            "brief_description": "Bhimpalasi has the strongest evidence base for afternoon anxiety reduction.",
            "musical_features": {"notes": "Sa Ga♭ Ma Pa Ni♭ Sa", "vadi": "Ga", "samvadi": "Ni", "movement": "Gentle, serene"}
        },
        {
            "raga_name": "Kafi", "also_known_as": "Kafi Thaat",
            "time_of_day": "Night", "thaat": "Kafi",
            "arousal_level": 0.42, "valence": 0.75, "tempo_bpm": 65,
            "primary_emotion": "Joy", "secondary_emotion": "Lightness",
            "stress_reduction": 0.78, "anxiety_relief": 0.75,
            "depression_help": 0.88, "sleep_induction": 0.70,
            "pain_relief": 0.65, "focus_enhancement": 0.72,
            "emotional_stability": 0.80, "blood_pressure_reduction": 0.68,
            "immune_boost": 0.75, "spiritual_uplift": 0.78,
            "therapy_evidence_score": 0.82, "popularity_score": 0.78,
            "research_citations": 28, "frequency_hz": 264,
            "scale_type": "Heptatonic", "mood_color": "Spring Green",
            "chakra": "Manipura",
            "target_conditions": ["Depression", "Seasonal Affective Disorder", "Low Mood", "Fatigue"],
            "contraindications": [],
            "brief_description": "Kafi's playful nature gives it an inherent mood-lifting quality suitable for depressive states.",
            "musical_features": {"notes": "Sa Re Ga♭ Ma Pa Dha Ni♭ Sa", "vadi": "Pa", "samvadi": "Sa", "movement": "Playful, oscillating"}
        },
    ]

    disease_map = {
        "anxiety": {
            "stress_score": 0.85, "sleep_disruption": 0.80, "mood_score": 0.25,
            "relaxation_need": 0.90, "emotional_stability_need": 0.88,
            "focus_need": 0.70, "energy_level": 0.30, "pain_level": 0.40,
            "arousal_preference": "low", "valence_preference": "high",
            "keywords": ["anxiety", "anxious", "worry", "nervous", "fear", "panic", "stress", "restless"]
        },
        "depression": {
            "stress_score": 0.70, "sleep_disruption": 0.85, "mood_score": 0.15,
            "relaxation_need": 0.85, "emotional_stability_need": 0.90,
            "focus_need": 0.65, "energy_level": 0.20, "pain_level": 0.50,
            "arousal_preference": "medium", "valence_preference": "high",
            "keywords": ["depression", "depressed", "sad", "hopeless", "empty", "grief", "melancholy"]
        },
        "insomnia": {
            "stress_score": 0.60, "sleep_disruption": 0.95, "mood_score": 0.45,
            "relaxation_need": 0.90, "emotional_stability_need": 0.75,
            "focus_need": 0.60, "energy_level": 0.30, "pain_level": 0.30,
            "arousal_preference": "very_low", "valence_preference": "neutral",
            "keywords": ["insomnia", "sleepless", "can't sleep", "sleep problem", "awake", "night", "tired"]
        },
        "stress": {
            "stress_score": 0.95, "sleep_disruption": 0.78, "mood_score": 0.30,
            "relaxation_need": 0.95, "emotional_stability_need": 0.80,
            "focus_need": 0.75, "energy_level": 0.45, "pain_level": 0.50,
            "arousal_preference": "low", "valence_preference": "high",
            "keywords": ["stress", "stressed", "pressure", "overwhelmed", "tension", "strain", "burnout"]
        },
        "ptsd": {
            "stress_score": 0.90, "sleep_disruption": 0.88, "mood_score": 0.20,
            "relaxation_need": 0.92, "emotional_stability_need": 0.95,
            "focus_need": 0.68, "energy_level": 0.25, "pain_level": 0.60,
            "arousal_preference": "very_low", "valence_preference": "high",
            "keywords": ["ptsd", "trauma", "traumatic", "flashback", "nightmare", "trigger", "abuse"]
        },
    }

    return raga_kb, disease_map


# ================================================================
# RECOMMENDATION ENGINE
# ================================================================

class StreamlitRagaEngine:
    """Lightweight recommendation engine for Streamlit."""

    def __init__(self, raga_kb, disease_map):
        self.raga_kb = raga_kb
        self.disease_map = disease_map

    def detect_conditions(self, text):
        """Simple keyword-based condition detection."""
        text_lower = text.lower()
        tokens = set(text_lower.replace(",", " ").replace(".", " ").split())
        results = []

        for condition, features in self.disease_map.items():
            match_count = 0
            for kw in features.get("keywords", []):
                if kw in text_lower:
                    match_count += 2
                elif any(kw in token or token in kw for token in tokens):
                    match_count += 1
            if match_count > 0:
                score = min(match_count / (len(features["keywords"]) * 0.3), 1.0)
                results.append({"condition": condition, "score": score})

        for condition in self.disease_map:
            if condition in text_lower and not any(r["condition"] == condition for r in results):
                results.append({"condition": condition, "score": 0.9})

        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    def extract_features(self, text):
        """Extract aggregated disease features."""
        matches = self.detect_conditions(text)

        if not matches:
            return {
                "stress_score": 0.4, "sleep_disruption": 0.35, "mood_score": 0.65,
                "relaxation_need": 0.6, "emotional_stability_need": 0.65,
                "focus_need": 0.65, "energy_level": 0.65, "pain_level": 0.2,
                "arousal_preference": "medium", "valence_preference": "high",
                "detected_conditions": ["general wellness"],
            }

        top = matches[:3]
        total = sum(m["score"] for m in top)
        weights = [m["score"] / total for m in top]

        feature_keys = [
            "stress_score", "sleep_disruption", "mood_score",
            "relaxation_need", "emotional_stability_need",
            "focus_need", "energy_level", "pain_level",
        ]

        aggregated = {k: 0.0 for k in feature_keys}
        arousal_prefs = []
        valence_prefs = []

        for i, match in enumerate(top):
            cond = self.disease_map.get(match["condition"], {})
            w = weights[i]
            for k in feature_keys:
                aggregated[k] += cond.get(k, 0.5) * w
            arousal_prefs.append(cond.get("arousal_preference", "medium"))
            valence_prefs.append(cond.get("valence_preference", "high"))

        from collections import Counter
        aggregated["arousal_preference"] = Counter(arousal_prefs).most_common(1)[0][0]
        aggregated["valence_preference"] = Counter(valence_prefs).most_common(1)[0][0]
        aggregated["detected_conditions"] = [m["condition"] for m in top]

        return aggregated

    def recommend(self, text):
        """Generate recommendation."""
        features = self.extract_features(text)
        results = []

        arousal_map = {"very_low": 0.2, "low": 0.35, "medium": 0.55, "high": 0.75}
        target_arousal = arousal_map.get(features.get("arousal_preference", "low"), 0.35)

        for raga in self.raga_kb:
            # Relaxation
            arousal_match = 1.0 - abs(raga["arousal_level"] - target_arousal)
            relaxation_score = (
                features.get("relaxation_need", 0.5) * raga.get("stress_reduction", 0.5) * 0.5
                + features.get("stress_score", 0.5) * raga.get("stress_reduction", 0.5) * 0.3
                + arousal_match * 0.2
            )

            # Emotional
            emotional_score = (
                features.get("emotional_stability_need", 0.5) * raga.get("emotional_stability", 0.5) * 0.5
                + features.get("mood_score", 0.5) * (1 - raga.get("valence", 0.5)) * 0.2
                + raga.get("valence", 0.5) * 0.3
            )

            # Evidence
            evidence_score = raga.get("therapy_evidence_score", 0.5)

            # Acoustic
            acoustic_score = (
                features.get("sleep_disruption", 0.5) * raga.get("sleep_induction", 0.5) * 0.35
                + features.get("pain_level", 0.5) * raga.get("pain_relief", 0.5) * 0.35
                + features.get("focus_need", 0.5) * raga.get("focus_enhancement", 0.5) * 0.3
            )

            # Similarity
            detected = features.get("detected_conditions", [])
            targets = raga.get("target_conditions", [])
            if detected and targets:
                match_count = sum(
                    1 for dc in detected
                    for tc in targets
                    if dc.lower() in tc.lower() or tc.lower() in dc.lower()
                )
                similarity_score = match_count / max(len(detected), 1)
            else:
                similarity_score = 0.5

            total = (
                relaxation_score * 0.30
                + emotional_score * 0.25
                + evidence_score * 0.20
                + acoustic_score * 0.15
                + similarity_score * 0.10
            )

            results.append(
                {
                    "raga": raga,
                    "total_score": total,
                    "factor_scores": {
                        "relaxation_profile": relaxation_score,
                        "emotional_stabilization": emotional_score,
                        "therapy_evidence": evidence_score,
                        "acoustic_match": acoustic_score,
                        "similarity_score": similarity_score,
                    },
                }
            )

        results.sort(key=lambda x: x["total_score"], reverse=True)

        top = results[0]
        confidence = round(top["total_score"] * 100, 1)

        supporting = []
        fs = top["factor_scores"]
        if fs["relaxation_profile"] > 0.7:
            supporting.append("Relaxation profile")
        if fs["emotional_stabilization"] > 0.7:
            supporting.append("Emotional stabilization")
        if fs["therapy_evidence"] > 0.7:
            supporting.append("Positive therapy evidence")
        if fs["acoustic_match"] > 0.7:
            supporting.append("Low-arousal acoustic characteristics")
        if fs["similarity_score"] > 0.5:
            supporting.append("Similarity to historical recommendations")

        return {
            "recommended_raga": top,
            "confidence": confidence,
            "supporting_factors": supporting,
            "alternative_ragas": results[1:5],
            "detected_conditions": features.get("detected_conditions", []),
            "extracted_features": features,
        }


# ================================================================
# MAIN UI
# ================================================================

def main():
    # Load data
    raga_kb, disease_map = load_knowledge_base()
    engine = StreamlitRagaEngine(raga_kb, disease_map)

    # Header
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown(
            '<div style="background:linear-gradient(135deg,#F59E0B,#EA580C);width:60px;height:60px;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:28px;">🎵</div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown('<p class="main-header">RagaTherapy</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="sub-header">AI-Powered Disease-Aware Raga Recommendation System</p>',
            unsafe_allow_html=True,
        )

    # Input
    st.markdown("### Describe your symptoms or condition")
    user_input = st.text_area(
        "Input",
        placeholder='e.g., "I have anxiety and stress", "I am unable to sleep", "I feel depressed and restless"...',
        label_visibility="collapsed",
        height=100,
    )

    # Example buttons
    examples = [
        "I have anxiety and stress",
        "I am unable to sleep",
        "I feel depressed and restless",
        "I have high stress levels",
    ]
    cols = st.columns(len(examples))
    for i, example in enumerate(examples):
        with cols[i]:
            if st.button(example, key=f"ex_{i}", use_container_width=True):
                user_input = example
                st.rerun()

    if st.button("🎵 Recommend Raga", type="primary", use_container_width=True):
        if not user_input.strip():
            st.error("Please enter a symptom, disease, or condition description.")
        else:
            with st.spinner("Analyzing symptoms and finding the best raga..."):
                result = engine.recommend(user_input.strip())

            st.markdown("---")

            # Detected Conditions
            st.markdown("### 🔍 NLP Analysis — Detected Conditions")
            conds = result["detected_conditions"]
            cols = st.columns(len(conds) if conds else 1)
            for i, cond in enumerate(conds):
                with cols[i]:
                    st.markdown(
                        f'<div style="background:#FEF3C7;border:1px solid #F59E0B;border-radius:12px;padding:12px;text-align:center;font-weight:600;">{cond.title()}</div>',
                        unsafe_allow_html=True,
                    )
            st.markdown("")

            # Main Recommendation
            top = result["recommended_raga"]
            raga = top["raga"]

            rec_col1, rec_col2 = st.columns([3, 1])
            with rec_col1:
                st.markdown(f"## 🎵 Recommended Raga: **{raga['raga_name']}**")
                st.markdown(f"*Also known as {raga['also_known_as']}*")
                st.markdown(
                    f"🕐 **{raga['time_of_day']}** | 🎼 **{raga['thaat']}** | 💫 **{raga['primary_emotion']}** | ⚡ **{raga['tempo_bpm']} BPM**"
                )
                st.markdown(f"**Scale:** {raga['scale_type']} | **Mood:** {raga['mood_color']} | **Chakra:** {raga['chakra']}")
                st.markdown(f"**Notes:** {raga['musical_features']['notes']}")
                st.markdown(f"**Vadi:** {raga['musical_features']['vadi']} | **Samvadi:** {raga['musical_features']['samvadi']}")
            with rec_col2:
                color = "#059669" if result["confidence"] >= 90 else "#D97706" if result["confidence"] >= 75 else "#DC2626"
                st.markdown(
                    f'<div style="background:{color};color:white;border-radius:50%;width:100px;height:100px;display:flex;align-items:center;justify-content:center;text-align:center;margin:auto;"><div><span style="font-size:24px;font-weight:800;">{result["confidence"]}%</span><br><span style="font-size:10px;">Confidence</span></div></div>',
                    unsafe_allow_html=True,
                )

            st.markdown(f"*{raga['brief_description']}*")
            st.markdown(f"📚 Based on **{raga['research_citations']}** research citations")

            # Supporting Factors
            st.markdown("### ✅ Supporting Factors")
            factor_icons = {
                "Relaxation profile": "🧘",
                "Emotional stabilization": "💙",
                "Positive therapy evidence": "📊",
                "Low-arousal acoustic characteristics": "🔉",
                "Similarity to historical recommendations": "📜",
            }
            factor_cols = st.columns(len(result["supporting_factors"]))
            for i, factor in enumerate(result["supporting_factors"]):
                with factor_cols[i]:
                    icon = factor_icons.get(factor, "✔️")
                    st.markdown(
                        f'<div class="factor-item"><span style="font-size:20px;">{icon}</span><br><strong>{factor}</strong></div>',
                        unsafe_allow_html=True,
                    )

            # Alternative Ragas
            st.markdown("### 🔄 Alternative Ragas")
            alt_cols = st.columns(min(4, len(result["alternative_ragas"])))
            for i, alt in enumerate(result["alternative_ragas"]):
                with alt_cols[i]:
                    st.markdown(
                        f'<div class="alt-raga-card"><strong>{alt["raga"]["raga_name"]}</strong><br>'
                        f'<span style="color:#F59E0B;font-weight:700;">{round(alt["total_score"]*100, 1)}%</span><br>'
                        f'<small>{alt["raga"]["primary_emotion"]} • {alt["raga"]["time_of_day"]}</small></div>',
                        unsafe_allow_html=True,
                    )

            # Explanation
            st.markdown("### 📖 Clinical Explanation")
            mf = raga["musical_features"]
            features = result["extracted_features"]
            explanation = (
                f"{raga['raga_name']} (also known as {raga['also_known_as']}) is a {raga['thaat']} thaat raga "
                f"performed during {raga['time_of_day'].lower()}. With a primary emotion of "
                f"{raga['primary_emotion'].lower()} and a tempo of {raga['tempo_bpm']} BPM, "
                f"it creates a {'calming' if raga['arousal_level'] < 0.35 else 'balanced' if raga['arousal_level'] < 0.5 else 'energizing'} "
                f"sonic environment. "
                f"The raga's musical structure ({mf.get('notes', 'N/A')}) with vadi {mf.get('vadi', 'N/A')} "
                f"and samvadi {mf.get('samvadi', 'N/A')} creates {mf.get('movement', 'N/A').lower()} movement. "
                f"This recommendation carries a {result['confidence']}% therapeutic match score based on "
                f"{raga['research_citations']} research citations."
            )
            st.markdown(explanation)

            # Feature Comparison
            st.markdown("### 📊 Patient-Raga Feature Comparison")
            comp_data = {
                "Metric": [
                    "Stress", "Sleep", "Mood", "Relaxation", "Emo. Stability", "Focus",
                ],
                "Patient Need": [
                    features.get("stress_score", 0) * 100,
                    features.get("sleep_disruption", 0) * 100,
                    (1 - features.get("mood_score", 0)) * 100,
                    features.get("relaxation_need", 0) * 100,
                    features.get("emotional_stability_need", 0) * 100,
                    features.get("focus_need", 0) * 100,
                ],
                f"{raga['raga_name']} Score": [
                    raga.get("stress_reduction", 0) * 100,
                    raga.get("sleep_induction", 0) * 100,
                    raga.get("depression_help", 0) * 100,
                    raga.get("stress_reduction", 0) * 100,
                    raga.get("emotional_stability", 0) * 100,
                    raga.get("focus_enhancement", 0) * 100,
                ],
            }
            comp_df = pd.DataFrame(comp_data).set_index("Metric")
            st.bar_chart(comp_df)


if __name__ == "__main__":
    main()
