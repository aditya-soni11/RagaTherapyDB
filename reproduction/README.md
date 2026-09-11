# Reproduction Pipeline

A self-contained, working re-implementation of the paper's methodology
(Section 4: Multi-Factor Scoring Engine; Section 6: Experimental Setup).
Added because the original Colab orchestration files referenced by
`notebooks/run_local.py` were lost prior to archiving — see `SETUP_GUIDE.md`
for the supported ways to run this project.

## Files

- `parse_knowledge_base.py` — parses the authoritative knowledge base
  directly from `../src/data/ragaKnowledgeBase.ts` and
  `../src/data/diseaseFeatureMap.ts`, producing `ragas_parsed.json`
  (30 r̄agas) and `diseases_parsed.json` (23 conditions). Already run once
  — re-run this if you edit the TypeScript source files.
- `reproduce_pipeline.py` — the full pipeline: implements the exact
  five-factor scoring formulas from the paper, generates the synthetic
  training dataset (12 base templates × 8 Gaussian-noise draws per
  condition + 80 co-morbidity blends → 2,288 samples), trains XGBoost
  (300 estimators, depth 8) and an MLP (128→256→128→64), evaluates
  in-distribution performance against a majority baseline, and runs
  Leave-One-Condition-Out (LOCO) cross-validation across all 23
  conditions.
- `ragas_parsed.json`, `diseases_parsed.json` — parsed knowledge base
  (outputs of `parse_knowledge_base.py`, checked in for convenience).
- `synthetic_dataset.csv` — the generated training dataset from the last run.
- `reproduction_results.json` — in-distribution metrics + full per-condition
  LOCO breakdown from the last run.

## Usage

```bash
pip install -r requirements.txt
python parse_knowledge_base.py   # regenerate knowledge base JSON (optional, already included)
python reproduce_pipeline.py     # run the full pipeline (~1-2 min on CPU)
```

## Expected output vs. paper

This is an independent re-implementation, not the original lost code, so
exact figures will differ slightly from the paper's published numbers while
showing the same qualitative pattern:

| Metric | Paper | Typical re-run |
|---|---|---|
| Dataset size | 2,288 | 2,288 (exact — this part is deterministic) |
| XGBoost in-distribution accuracy | 86.03% | ~83–86% |
| MLP in-distribution accuracy | 84.93% | ~83–85% |
| Mean LOCO accuracy | 0.2935 | ~0.22–0.29 |
| Conditions with 0.0000 LOCO accuracy | 6 (panic disorder, chronic pain, heart disease, dementia, IBS, loneliness) | same 6, sometimes a few more |

The paper reports its own original run's figures, consistent with the
"Provenance and Re-implementation Disclosure" section of the manuscript.
This script exists so the methodology is genuinely runnable and inspectable,
not to force-match the published numbers.
