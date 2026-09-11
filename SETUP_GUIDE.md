# RagaTherapy — Complete Setup Guide

## How to Run This Project

You have **3 options**:

---

## OPTION 1: Run the Web Application

```bash
git clone https://github.com/aditya-soni11/RagaTherapyDB.git
cd RagaTherapyDB
npm install
npm run dev
```
Open the local URL printed in your terminal. Enter a free-text symptom
description and the app returns ranked r̄aga recommendations with a full
scoring breakdown.

To build for production:
```bash
npm run build
```

---

## OPTION 2: Run the Streamlit Dashboard

```bash
pip install streamlit pandas
streamlit run app/app.py
```
Useful for exploring how sliding individual symptom scores changes the
recommended r̄aga ranking in real time — geared toward music therapists and
researchers rather than end users.

---

## OPTION 3: Reproduce the Paper's Results (Python)

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
  recall, F1, top-3 accuracy, LOCO cross-validation) for both an XGBoost and
  an MLP classifier.

See `reproduction/README.md` for how these figures compare to the paper's
published numbers.

---

## Troubleshooting

### "ModuleNotFoundError" when running the reproduction pipeline
```bash
pip install -r reproduction/requirements.txt
```

### Web app: blank page or build errors
```bash
rm -rf node_modules
npm install
```

---

## File Overview

```
├── src/                      # React + TypeScript web application
│   ├── data/                   → R̄aga knowledge base (30 ragas) &
│   │                              disease-feature map (23 conditions)
│   ├── engine/                  → Scoring / recommendation engine
│   └── components/              → UI components
├── app/app.py                # Streamlit dashboard for therapists & researchers
├── notebooks/                 # Colab notebooks for the ML pipeline
├── reproduction/              # Standalone Python reproduction of the paper's
│                                 dataset generation, model training, and LOCO evaluation
├── reports/                    # Project notes and research report
├── PROJECT_STRUCTURE.md
└── package.json / vite.config.ts / tsconfig.json
```
