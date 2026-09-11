# RagaTherapy — Project Structure

```
RagaTherapyDB/
├── index.html                          # Entry HTML
├── package.json                        # Dependencies
├── vite.config.ts                      # Vite config
├── tsconfig.json                       # TypeScript config
│
├── src/                                # React web app source
│   ├── main.tsx                        # React entry
│   ├── App.tsx                         # App component
│   ├── index.css                       # Tailwind styles
│   ├── data/                           # Embedded knowledge bases
│   │   ├── ragaKnowledgeBase.ts        # 30 ragas with full therapeutic features
│   │   └── diseaseFeatureMap.ts        # 23 disease condition mappings
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
├── reproduction/                       # Standalone reproduction pipeline
│   ├── parse_knowledge_base.py         # Parses src/data/*.ts → JSON
│   ├── reproduce_pipeline.py           # Dataset generation, model training, LOCO eval
│   ├── ragas_parsed.json               # Parsed knowledge base (30 ragas)
│   ├── diseases_parsed.json            # Parsed condition map (23 conditions)
│   ├── synthetic_dataset.csv           # Generated training dataset (output)
│   ├── reproduction_results.json       # Evaluation metrics (output)
│   ├── requirements.txt
│   └── README.md                       # Reproduction scope + expected variance vs. paper
│
├── notebooks/                          # Colab notebook(s)
│   ├── RagaTherapy.ipynb
│   ├── RagaTherapy_CellByCell.ipynb
│   ├── ragatherapy_colab.py            # Standalone Colab script
│   ├── generate_notebook.py
│   └── run_local.py                    # Local desktop runner
│
├── reports/                            # Reports and metrics
│   └── README.md                       # Research report
│
└── dist/                                # Built web app (generated)
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
pip install streamlit pandas
streamlit run app/app.py
```

### Reproduce the Paper's Results
```bash
cd reproduction
pip install -r requirements.txt
python parse_knowledge_base.py
python reproduce_pipeline.py
```
