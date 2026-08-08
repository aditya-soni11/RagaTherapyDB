# RagaTherapy — Project Structure

```
ragatherapy/
├── index.html                          # Entry HTML
├── package.json                        # Dependencies
├── vite.config.ts                      # Vite config
├── tsconfig.json                       # TypeScript config
│
├── data/                               # Data files (generated in Colab)
│   ├── raw/                            # Raw downloaded datasets
│   │   ├── symptom_disease_train.csv
│   │   ├── symptom_disease_test.csv
│   │   ├── disease_description.csv
│   │   ├── disease_precaution.csv
│   │   └── mental_health_features.csv
│   ├── processed/                      # Cleaned datasets
│   │   ├── symptom_disease_clean.csv
│   │   ├── raga_knowledge_base_clean.csv
│   │   ├── mental_health_features_clean.csv
│   │   └── training_data.csv
│   └── knowledge_base/                 # Knowledge bases
│       ├── raga_knowledge_base.csv
│       ├── raga_knowledge_base.json
│       └── disease_feature_map.json
│
├── models/                             # Trained models
│   ├── nlp/
│   ├── recommendation/
│   │   ├── xgboost_raga_model.pkl
│   │   └── label_encoder.pkl
│   ├── explainability/
│   ├── ragatherapy_complete.pkl
│   ├── deployment_config.json
│   └── version_info.json
│
├── notebooks/                          # Colab notebook
│   └── ragatherapy_colab.py            # Complete Colab notebook (all 15 sections)
│
├── src/                                # React web app source
│   ├── main.tsx                        # React entry
│   ├── App.tsx                         # App component
│   ├── index.css                       # Tailwind styles
│   ├── data/                           # Embedded knowledge bases
│   │   ├── ragaKnowledgeBase.ts        # 28 ragas with full therapeutic features
│   │   └── diseaseFeatureMap.ts        # 20+ disease condition mappings
│   ├── engine/                         # Recommendation engine
│   │   └── recommendationEngine.ts     # NLP + Feature extraction + Ranking
│   └── components/                     # React UI components
│       ├── RagaTherapy.tsx             # Main app container
│       ├── RagaCard.tsx                # Raga recommendation card
│       ├── SupportingFactors.tsx       # Supporting factors display
│       ├── AlternativeRagas.tsx        # Alternative ragas grid
│       ├── DetectedConditions.tsx      # NLP-detected conditions
│       └── FeatureRadar.tsx            # Patient-Raga feature comparison
│
├── app/                                # Streamlit deployment
│   └── app.py                          # Complete Streamlit application
│
├── reports/                            # Reports and metrics
│   ├── README.md                       # Research report
│   └── figures/                        # Generated figures
│       ├── therapeutic_score_distribution.png
│       ├── correlation_heatmap.png
│       ├── top_ragas_by_condition.png
│       ├── arousal_valence_space.png
│       ├── mental_health_features.png
│       ├── shap_summary.png
│       ├── shap_importance.png
│       └── shap_waterfall.png
│
└── dist/                               # Built web app (generated)
    └── index.html                      # Single-file production build
```

## Quick Start

### Web App (React + Vite + Tailwind)
```bash
npm install
npm run dev          # Development server
npm run build        # Production build → dist/
```

### Streamlit App
```bash
pip install streamlit pandas numpy
streamlit run app/app.py
```

### Colab Notebook
Upload `notebooks/ragatherapy_colab.py` to Google Colab and run all sections sequentially.
