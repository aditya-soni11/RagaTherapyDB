"""
Regenerates ragas_parsed.json and diseases_parsed.json directly from the
authoritative source files at ../src/data/ragaKnowledgeBase.ts and
../src/data/diseaseFeatureMap.ts.

Run this first if you've edited the knowledge base and want
reproduce_pipeline.py to pick up the changes:

    python parse_knowledge_base.py
    python reproduce_pipeline.py
"""
import re
import json
import os

SRC_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "data")


def parse_ragas():
    content = open(os.path.join(SRC_DIR, "ragaKnowledgeBase.ts")).read()
    blocks = re.split(r"\n  \{\n", content)[1:]
    ragas = []
    for b in blocks:
        b = "  {\n" + b

        def grab(field):
            m = re.search(rf'{field}:\s*"([^"]*)"', b)
            if m:
                return m.group(1)
            m = re.search(rf"{field}:\s*([\d.]+)", b)
            if m:
                return float(m.group(1))
            return None

        def grab_list(field):
            m = re.search(rf"{field}:\s*\[([^\]]*)\]", b)
            if not m:
                return []
            return re.findall(r'"([^"]*)"', m.group(1))

        name = grab("raga_name")
        if not name:
            continue
        ragas.append(
            {
                "raga_name": name,
                "arousal_level": grab("arousal_level"),
                "valence": grab("valence"),
                "stress_reduction": grab("stress_reduction"),
                "sleep_induction": grab("sleep_induction"),
                "pain_relief": grab("pain_relief"),
                "focus_enhancement": grab("focus_enhancement"),
                "emotional_stability": grab("emotional_stability"),
                "therapy_evidence_score": grab("therapy_evidence_score"),
                "target_conditions": grab_list("target_conditions"),
                "contraindications": grab_list("contraindications"),
            }
        )
    return ragas


def parse_diseases():
    content = open(os.path.join(SRC_DIR, "diseaseFeatureMap.ts")).read()
    pattern = re.compile(r'\n  "?([\w ]+?)"?: \{(.*?)\n  \},', re.DOTALL)
    matches = pattern.findall(content)

    FEATS = [
        "stress_score",
        "sleep_disruption",
        "mood_score",
        "relaxation_need",
        "emotional_stability_need",
        "focus_need",
        "energy_level",
        "pain_level",
    ]
    diseases = {}
    for key, body in matches:
        key = key.strip()

        def grab(field):
            m = re.search(rf"{field}:\s*([\d.]+)", body)
            return float(m.group(1)) if m else None

        diseases[key] = {f: grab(f) for f in FEATS}
    return diseases


if __name__ == "__main__":
    ragas = parse_ragas()
    diseases = parse_diseases()
    print(f"Parsed {len(ragas)} ragas and {len(diseases)} conditions from src/data/")

    json.dump(ragas, open("ragas_parsed.json", "w"), indent=2)
    json.dump(diseases, open("diseases_parsed.json", "w"), indent=2)
    print("Wrote ragas_parsed.json and diseases_parsed.json")
