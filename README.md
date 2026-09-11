# RagaTherapy

**AI-powered, disease-aware recommendation of Indian classical r̄agas for music therapy.**

RagaTherapy maps free-text descriptions of physical or psychological symptoms
to therapeutically appropriate Hindustani classical r̄agas, using a curated
musicological knowledge base, a hybrid NLP condition-detection layer, and a
five-factor explainable scoring engine with a hard clinical safety
(contraindication) override. This repository is the companion codebase for
the paper *"RagaTherapyDB: A Fine-tuning Benchmark on Label Circularity and
Generalization in Music Therapy Recommendation."*

## Overview

- **30 r̄agas**, each profiled across arousal, valence, stress reduction,
  sleep induction, pain relief, focus enhancement, emotional stability,
  therapy evidence level, target conditions, and contraindications.
- **23 clinical conditions**, each mapped to an 8-dimensional target feature
  profile (stress, sleep disruption, mood, relaxation need, emotional
  stability need, focus need, energy level, pain level) plus an NLP keyword
  set.
- **Hybrid NLP layer** combining keyword/n-gram matching with Sentence-BERT
  semantic similarity to detect conditions from natural-language input
  (Sentence-BERT stage described in `reports/README.md` Section 4.1; the
  deployed web app and Streamlit dashboard currently run the keyword/n-gram
  layer only).
- **Five-factor scoring engine** (relaxation matching, emotional stability,
  therapeutic evidence, acoustic match, condition similarity) with an
  absolute safety layer that zeroes out any r̄aga contraindicated for a
  detected condition.
- **ML approximation layer** (XGBoost, MLP) trained to replicate the rule
  engine's decision surface for low-latency deployment, evaluated with both
  standard in-distribution metrics and Leave-One-Condition-Out (LOCO)
  cross-validation to test genuine generalization.

## Repository structure

```
├── src/                      # React + TypeScript web application
│   ├── data/                   → R̄aga knowledge base & disease-feature map
│   ├── engine/                  → Scoring / recommendation engine
│   └── components/              → UI components
├── app/app.py                # Streamlit dashboard for therapists & researchers
├── notebooks/                 # Colab notebooks for the full ML pipeline
├── reproduction/              # Standalone Python reproduction of the paper's
│                                 dataset generation, model training, and LOCO evaluation
├── reports/                    # Project notes and research report
├── PROJECT_STRUCTURE.md
├── SETUP_GUIDE.md
└── package.json / vite.config.ts / tsconfig.json
```

## Getting started

### Web application

```bash
npm install
npm run dev
```

### Streamlit dashboard

```bash
pip install streamlit pandas
streamlit run app/app.py
```

### Reproducing the paper's results

```bash
cd reproduction
pip install -r requirements.txt
python reproduce_pipeline.py
```

This regenerates the knowledge base from `src/data/`, builds the synthetic
training dataset, trains the XGBoost and MLP classifiers, and runs the full
23-condition Leave-One-Condition-Out cross-validation described in the
paper's Methodology and Experimental Setup sections. See
[`reproduction/README.md`](reproduction/README.md) for details on how this
run relates to the exact figures published in the paper.



## 1. Run the web application

```bash
git clone https://github.com/aditya-soni11/RagaTherapyDB.git
cd RagaTherapyDB
npm install
npm run dev
```

Open the local URL printed in your terminal. Enter a free-text symptom
description and the app will detect matching conditions and return ranked
r̄aga recommendations with a full scoring breakdown.

To build for production:

```bash
npm run build
```

---

## 2. Run the Streamlit dashboard

```bash
pip install streamlit pandas
streamlit run app/app.py
```

Useful for exploring how sliding individual symptom scores changes the
recommended r̄aga ranking in real time — geared toward music therapists and
researchers rather than end users.

---

## 3. Use the Python pipeline (dataset generation, model training, evaluation)

```bash
cd reproduction
pip install -r requirements.txt
python parse_knowledge_base.py   # parses src/data/ into JSON
python reproduce_pipeline.py     # generates dataset, trains models, evaluates
```

This produces:
- `synthetic_dataset.csv` — a generated training dataset mapping symptom
  feature vectors to recommended r̄agas.
- `reproduction_results.json` — evaluation metrics (accuracy, precision,
  recall, F1, top-3 accuracy) for both an XGBoost and an MLP classifier.

---

## 4. Use the knowledge base or scoring engine in your own project

### Option A — Use the raw data

The knowledge base is plain, dependency-free data you can import into any
stack:

- `src/data/ragaKnowledgeBase.ts` — 30 r̄aga entries
- `src/data/diseaseFeatureMap.ts` — 23 condition entries

For non-TypeScript projects, run the parser to get clean JSON:

```bash
cd reproduction
python parse_knowledge_base.py
```

This writes `ragas_parsed.json` and `diseases_parsed.json`, which you can
load in Python, JavaScript, or any language with JSON support.

### Option B — Use the scoring engine (TypeScript)

```ts
import { recommendRaga } from './src/engine/recommendationEngine';

const result = recommendRaga("I've been feeling anxious and can't sleep");
console.log(result); // detected conditions + ranked list of ragas with scores
```

`recommendRaga` runs the full pipeline internally — condition detection
(`detectConditions`), feature extraction (`extractDiseaseFeatures`), and
scoring — and returns a `RecommendationResult`. If you only need a specific
step, `detectConditions` and `extractDiseaseFeatures` are also exported
individually from the same file.

### Option C — Use the scoring logic in Python

`reproduction/reproduce_pipeline.py` includes a Python implementation of
the same five-factor scoring formulas (`score_raga`,
`best_raga_for_profile`). Import these directly if you want the scoring
engine without the training/evaluation code around it:

```python
import json
from reproduce_pipeline import score_raga, best_raga_for_profile

ragas = json.load(open('ragas_parsed.json'))
diseases = json.load(open('diseases_parsed.json'))

# Build a patient profile from one or more detected conditions
condition = 'anxiety'
profile = diseases[condition]

best_raga, all_scores = best_raga_for_profile(profile, [condition])
print(best_raga)
```

---


## Knowledge base

The r̄aga knowledge base and disease-feature map live in
[`src/data/ragaKnowledgeBase.ts`](src/data/ragaKnowledgeBase.ts) and
[`src/data/diseaseFeatureMap.ts`](src/data/diseaseFeatureMap.ts), and
correspond directly to Appendix A and Appendix B of the paper. They were
constructed from published musicological and music-therapy literature
(Deva 1981, Bagchee 1998, Nizamie & Tikka 2014, Thaut 2008, Sairam 2004,
and others cited in the paper), with numerical scores assigned by the
authors as relative, computationally usable rankings rather than clinically
measured values — this limitation is discussed in the paper.


## Requirements

- Node.js 18+ and npm (for the web app)
- Python 3.9–3.12 (for the Streamlit dashboard and reproduction pipeline)
- `pandas`, `numpy`, `scikit-learn`, `xgboost` (see `reproduction/requirements.txt`)


## Project link
https://raga-therapy-db.vercel.app/

## Citation

If you use this knowledge base, scoring engine, or code, please cite the
accompanying paper (full citation to be added upon publication).

## License

See [LICENSE](LICENSE) for details.
