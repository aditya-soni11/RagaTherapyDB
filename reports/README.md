# RagaTherapy — Research Report

## AI-Powered Disease-Aware Indian Classical Raga Recommendation System

---

## 1. Novelty Statement

RagaTherapy is a **knowledge-driven recommendation framework** that encodes therapeutic properties of Indian Classical Ragas into a computable multi-factor scoring model, augmented by NLP-based symptom understanding and ML/DL-based ranking. To our knowledge, this is the **first system** that:

1. Maps natural language disease/symptom descriptions to therapeutic raga recommendations through a structured multi-stage pipeline.
2. Uses a 5-factor scoring model (Relaxation, Emotional Stabilization, Therapy Evidence, Acoustic Match, Condition Similarity) grounded in music therapy theory.
3. Provides SHAP-based explainability for raga therapy recommendations.
4. Validates generalization through Leave-One-Condition-Out (LOCO) evaluation.

## 2. Research Gap

| Gap | Existing Work | Our Contribution |
|-----|--------------|------------------|
| Raga classification exists, but not disease-aware recommendation | Chordia & Rae (2013) classify ragas from audio | We recommend ragas FOR specific diseases |
| Music recommendation uses collaborative filtering | Spotify, YouTube Music | We use clinical feature vectors, not listening history |
| Music therapy literature is qualitative | Sairam (2004), Nizamie & Goyal (2010) | We operationalize qualitative claims into computable scores |
| No explainable AI for raga therapy | None found | We provide SHAP-based explanations |

## 3. Datasets

### 3.1 Raga Therapeutic Knowledge Base

| Property | Value |
|----------|-------|
| **Size** | 30 ragas × 20+ features |
| **Type** | Expert-curated knowledge base |
| **Construction Method** | Structured scoring rubric applied to qualitative therapeutic properties documented in published musicological and music therapy sources |
| **Sources** | Deva (1981), Bagchee (1998), Chordia & Rae (2013), Nizamie & Goyal (2010), Thaut (2008), Sharma & Mathur (2011), Sairam (2004), Sundar (2007) |

**Scoring Methodology:**
- Each therapeutic dimension (stress_reduction, anxiety_relief, etc.) was assigned a score in [0.0, 1.0] by the authors
- Scores are based on: (a) raga's arousal-valence profile inferred from its melodic structure, (b) time-of-day and seasonal associations from raga theory, (c) emotional/rasa associations documented in musicological texts, (d) any available clinical evidence from music therapy literature
- **Limitation:** These scores represent author assessments, not clinically measured values. They should be interpreted as relative therapeutic rankings suitable for a computational framework, not as clinical efficacy probabilities.

### 3.2 Disease-Symptom Feature Map

| Property | Value |
|----------|-------|
| **Size** | 23 conditions × 10 features (8 numerical + 2 categorical + keyword list) |
| **Type** | Author-curated clinical feature profiles |
| **Construction Method** | Numerical features (stress, sleep disruption, mood, etc.) assigned based on published clinical characterizations of each condition from standard medical references |
| **Validation** | Directional validity: high-stress conditions (anxiety, PTSD) have high stress_score; sleep disorders (insomnia) have high sleep_disruption — consistent with clinical expectations |
| **Limitation:** | Exact numerical values are author estimates. Different clinicians might assign slightly different values. The keyword lists for NLP matching are manually curated. |

### 3.3 Symptom-Disease Dataset (External Reference)

| Property | Value |
|----------|-------|
| **Source** | GitHub: anujdutt9/Disease-Predictor (MIT License) |
| **Original Size** | ~4,920 × 133 |
| **Usage in this work** | Reference for symptom vocabulary. NOT used for model training. |
| **Note** | Downloaded for symptom keyword reference during NLP pipeline development. The trained ML models do NOT use this dataset as training input. |

### 3.4 Augmented Training Dataset

| Property | Value |
|----------|-------|
| **Size** | 2,288 × 9 |
| **Type** | Synthetically generated from Datasets 3.1 and 3.2 |
| **Generation Method** | 12 base clinical feature templates across 23 conditions, each with 8 Gaussian noise-injected variations (2,208 samples), plus 80 co-morbidity samples blended from randomly paired conditions |
| **Labels** | Each sample's target raga label was assigned by the 5-factor rule-based scoring engine |
| **Important Note** | Training labels are rule-engine-generated, not independently annotated. The ML/DL models learn to approximate the rule-based scorer. Consequently, high ML accuracy indicates successful rule approximation, not independent clinical validation. This circularity is addressed through LOCO validation (Section 5.4). |

## 4. Methodology

### 4.1 Stage 1: NLP Disease Understanding

**Keyword-based detection:**
- Text tokenization, n-gram generation (unigrams, bigrams, trigrams)
- Fuzzy keyword matching against 30 condition keyword sets
- Ranked condition detection with confidence scores

**Sentence-BERT semantic detection:**
- Pre-trained `all-MiniLM-L6-v2` model (384-dim embeddings)
- Cosine similarity between user input and 30 condition description embeddings
- **Not fine-tuned** on medical domain — limitation acknowledged

**Hybrid fusion:**
- 40% keyword score + 60% SBERT semantic score
- Top-3 conditions selected for feature aggregation

### 4.2 Stage 2: Disease Feature Mapping

Weighted aggregation of top-3 detected conditions into 8-dimensional therapeutic need vector:
```
feature[f] = Σ(weight_i × disease_map[condition_i][f])  for i in top_3
where weight_i = detection_score_i / Σ(scores)
```

Output: `[stress_score, sleep_disruption, mood_score, relaxation_need, emotional_stability_need, focus_need, energy_level, pain_level]`

### 4.3 Stage 3: Multi-Factor Raga Scoring

For each of 30 ragas, compute weighted therapeutic match score:

| Factor | Weight | What It Measures |
|--------|--------|-----------------|
| Relaxation Profile | 30% | Stress reduction × relaxation need + arousal alignment |
| Emotional Stabilization | 25% | Emotional stability match + mood-valence alignment |
| Therapy Evidence | 20% | Literature-based evidence score (from KB) |
| Acoustic Match | 15% | Sleep induction × sleep need + pain relief × pain + focus match |
| Condition Similarity | 10% | Target condition overlap between detected and raga KB |

**Safety Layer:** Contraindication checking — ragas with documented contraindications for detected conditions receive score = 0.

### 4.4 Stage 4: ML/DL Model Training

Four models trained on augmented data:

| Model | Architecture | Purpose |
|-------|-------------|---------|
| XGBoost | 300 trees, depth 8 | Baseline tabular classifier |
| DNN | 8→128→256→128→64→42 (PyTorch) | Deep classification |
| Autoencoder + XGBoost | AE: 8→32→16→4→16→32→8, then XGBoost on 8+4=12 features | Feature learning + classification |
| Ensemble | 50% DNN + 50% XGBoost probability fusion | Combined prediction |

### 4.5 Stage 5: Explainability

- SHAP TreeExplainer on XGBoost model
- Per-feature contribution analysis
- Natural language explanation generation

## 5. Evaluation

### 5.1 Standard Classification Metrics

| Model | Accuracy | Precision | Recall | F1 |
|-------|----------|-----------|--------|-----|
| XGBoost | Computed | Computed | Computed | Computed |
| DNN | Computed | Computed | Computed | Computed |
| AE-XGBoost | Computed | — | — | Computed |
| Ensemble | Computed | — | — | Computed |

*(Exact values generated at runtime — see `reports/metrics/evaluation_metrics.json`)*

### 5.2 Ranking Metrics

| Model | Top-1 | Top-3 | Top-5 | NDCG@5 | MRR |
|-------|-------|-------|-------|--------|-----|
| XGBoost | ✓ | ✓ | ✓ | ✓ | ✓ |
| DNN | ✓ | ✓ | ✓ | ✓ | ✓ |
| Ensemble | ✓ | ✓ | ✓ | ✓ | ✓ |

### 5.3 Visualizations Generated

1. Confusion matrices (XGBoost and DNN)
2. Top-K accuracy comparison bar chart
3. Per-class precision/recall/F1 chart
4. Comprehensive 4-model comparison chart
5. SHAP summary, importance, and waterfall plots
6. DNN training loss and validation accuracy curves
7. XGBoost feature importance
8. Raga arousal-valence scatter plot
9. Therapeutic score distribution histograms
10. Feature correlation heatmap

### 5.4 Leave-One-Condition-Out (LOCO) Validation

**Purpose:** Address circularity concern. If the model only memorized training rules, it would fail on conditions it never trained on. LOCO tests generalization.

**Method:** For each of 23 conditions, train on all other conditions, predict on the held-out condition. Measure whether the model recommends therapeutically sensible ragas for the unseen condition based purely on its feature profile.

**Result:** LOCO accuracy reported in `reports/metrics/loco_validation.json`

**Interpretation:** A high LOCO accuracy indicates the model learned meaningful feature-to-raga mappings (e.g., "high stress + low arousal preference → calming ragas") rather than memorizing "anxiety → Yaman" mappings.

### 5.5 Clinical Validity Check

10 canonical test inputs verified for correct condition detection and therapeutically appropriate raga recommendation.

## 6. Limitations (Stated Transparently)

1. **No clinical trial data.** All therapeutic scores are expert-estimated, not measured in patient studies. The system should be viewed as a decision-support tool, not a clinically validated treatment protocol.

2. **Circular training labels.** ML/DL models learn to approximate the rule-based scorer. Standard accuracy metrics measure rule approximation fidelity, not clinical efficacy. LOCO validation partially addresses this.

3. **Sentence-BERT not domain-adapted.** The NLP model uses general-purpose embeddings. Fine-tuning on medical text (using BioBERT, ClinicalBERT, or MedNLI) would improve semantic understanding of clinical descriptions.

4. **No audio signal processing.** The system recommends ragas by therapeutic metadata, not by analyzing actual audio features (MFCCs, spectrograms, chroma). Incorporating audio analysis would strengthen the acoustic matching component.

5. **Single-culture focus.** The knowledge base covers Hindustani (North Indian) ragas. Carnatic (South Indian) and cross-cultural music therapy systems are not included.

## 7. Future Work

1. **Clinical validation:** Partner with music therapy practitioners to validate raga-disease mappings through controlled studies.
2. **Medical NLP fine-tuning:** Fine-tune SBERT on medical NLI datasets (MedNLI, PubMedQA).
3. **Audio feature integration:** Extract MFCCs, spectrograms from raga recordings and incorporate into the scoring model.
4. **User study:** Conduct A/B testing with actual patients to measure therapeutic outcomes.
5. **Expert panel validation:** Have 3-5 music therapy practitioners independently score the raga KB to establish inter-rater reliability.

## 8. Reproducibility

- `src/data/` — The r̄aga knowledge base and disease-feature map, with scoring methodology documented inline and in Section 4 of the paper.
- `notebooks/` — Colab notebooks covering the full pipeline (data generation, NLP, model training, evaluation).
- `reproduction/` — A standalone Python script that regenerates the knowledge base, synthetic training data, and full in-distribution + Leave-One-Condition-Out evaluation end-to-end from `src/data/`.

## 9. Publication Targets

- IEEE International Conference on Computing, Communication and Intelligent Systems (ICCCIS)
- Springer Lecture Notes in Computer Science (LNCS) workshops
- Scopus-indexed conferences on AI in Healthcare / Music Informatics
