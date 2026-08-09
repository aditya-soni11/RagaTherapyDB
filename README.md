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
  semantic similarity to detect conditions from natural-language input.
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


## Project link
https://raga-therapy-db.vercel.app/

## Citation

If you use this knowledge base, scoring engine, or code, please cite the
accompanying paper (full citation to be added upon publication).

## License

See [LICENSE](LICENSE) for details.
