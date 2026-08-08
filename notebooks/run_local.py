#!/usr/bin/env python3
"""
RagaTherapy — Local Desktop Runner
===================================
Run this script to execute the COMPLETE pipeline locally.

Note: this runner orchestrates the full Colab pipeline via
`notebooks/ragatherapy_colab_cells.py`, `publication_enhancements.py`, and
`quality_fixes.py`. For a lighter-weight, standalone reproduction of the
paper's methodology — dataset generation, XGBoost/MLP training, and
Leave-One-Condition-Out cross-validation — that runs directly against the
knowledge base in `src/data/` without those companion files, see
`reproduction/reproduce_pipeline.py` at the repository root.

Usage:
    python notebooks/run_local.py

Prerequisites:
    pip install pandas numpy scikit-learn nltk sentence-transformers xgboost shap joblib matplotlib seaborn requests torch

Expected Runtime: 10-20 min (CPU), 5-10 min (GPU)
"""

import sys
import os

# Change to project root if running from notebooks/
if os.path.basename(os.getcwd()) == 'notebooks':
    os.chdir('..')
print(f"Working directory: {os.getcwd()}")

# ================================================================
# SECTION 1: INSTALL/IMPORT LIBRARIES
# ================================================================
print("\n" + "=" * 70)
print("SECTION 1: IMPORTING LIBRARIES")
print("=" * 70)

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for local
import matplotlib.pyplot as plt
matplotlib.rcParams['figure.dpi'] = 120
import seaborn as sns
import json
import re
import requests
import random
import warnings
warnings.filterwarnings('ignore')

import nltk
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    classification_report, confusion_matrix,
    top_k_accuracy_score, ndcg_score
)
from sklearn.dummy import DummyClassifier
from sentence_transformers import SentenceTransformer
import xgboost as xgb
import shap
import joblib

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(f"✅ All libraries imported")
print(f"   pandas {pd.__version__}, numpy {np.__version__}")
print(f"   PyTorch {torch.__version__}, Device: {device}")

# ================================================================
# SECTION 2: CREATE DIRECTORIES & DOWNLOAD DATASETS
# ================================================================
print("\n" + "=" * 70)
print("SECTION 2: SETUP DIRECTORIES & DOWNLOAD DATA")
print("=" * 70)

from pathlib import Path

dirs = [
    "data/raw", "data/processed", "data/knowledge_base",
    "models/nlp", "models/recommendation", "models/explainability",
    "reports/figures", "reports/metrics", "src", "app"
]
for d in dirs:
    Path(d).mkdir(parents=True, exist_ok=True)
print("✅ Directory structure created")

# Download symptom-disease dataset
urls = [
    ("data/raw/symptom_disease_train.csv",
     "https://raw.githubusercontent.com/anujdutt9/Disease-Predictor/master/dataset/training.csv"),
    ("data/raw/symptom_disease_test.csv",
     "https://raw.githubusercontent.com/anujdutt9/Disease-Predictor/master/dataset/testing.csv"),
    ("data/raw/disease_description.csv",
     "https://raw.githubusercontent.com/anujdutt9/Disease-Predictor/master/dataset/symptom_Description.csv"),
    ("data/raw/disease_precaution.csv",
     "https://raw.githubusercontent.com/anujdutt9/Disease-Predictor/master/dataset/symptom_precaution.csv"),
]

for filepath, url in urls:
    if not os.path.exists(filepath):
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(r.content)
                print(f"  ✓ Downloaded {filepath}")
            else:
                print(f"  ⚠ Failed {filepath}: HTTP {r.status_code}")
        except Exception as e:
            print(f"  ⚠ Failed {filepath}: {e}")
    else:
        print(f"  ✓ Already exists: {filepath}")

# Mental health features
mental_health_data = {
    'condition': ['Anxiety','Depression','Bipolar Disorder','PTSD','OCD',
                  'Schizophrenia','Insomnia','Stress','Panic Disorder','ADHD',
                  'Autism Spectrum','Eating Disorder','Addiction','Dementia','Hypertension',
                  'Diabetes','Chronic Pain','Migraine','Asthma','Heart Disease',
                  'Irritable Bowel Syndrome','Fibromyalgia','Cancer','Arthritis','Epilepsy'],
    'stress_score': [0.85,0.70,0.75,0.90,0.80,0.65,0.60,0.95,0.88,0.72,
                     0.55,0.78,0.82,0.45,0.88,0.65,0.75,0.80,0.70,0.85,
                     0.72,0.78,0.82,0.70,0.75],
    'sleep_disruption': [0.80,0.85,0.90,0.88,0.75,0.70,0.95,0.78,0.82,0.65,
                         0.60,0.72,0.80,0.88,0.70,0.55,0.78,0.85,0.50,0.65,
                         0.68,0.80,0.85,0.72,0.75],
    'mood_score': [0.25,0.15,0.30,0.20,0.35,0.25,0.45,0.30,0.22,0.40,
                   0.50,0.25,0.30,0.40,0.40,0.45,0.35,0.38,0.50,0.42,
                   0.40,0.30,0.25,0.38,0.42],
    'relaxation_need': [0.90,0.85,0.80,0.92,0.85,0.80,0.90,0.95,0.90,0.75,
                        0.70,0.82,0.78,0.65,0.88,0.72,0.85,0.82,0.78,0.88,
                        0.80,0.88,0.85,0.82,0.78],
    'emotional_stability_need': [0.88,0.90,0.92,0.95,0.88,0.92,0.75,0.80,0.90,0.82,
                                 0.85,0.88,0.85,0.70,0.75,0.65,0.80,0.72,0.65,0.78,
                                 0.72,0.82,0.88,0.78,0.85],
}
mental_df = pd.DataFrame(mental_health_data)
mental_df.to_csv("data/raw/mental_health_features.csv", index=False)
print(f"  ✓ Mental health features: {mental_df.shape}")
print("✅ All data ready")

# ================================================================
# SECTION 3: Now run the main notebook code
# ================================================================

# We import and exec each section from the main cells file.
# But since the file has !pip (shell commands), we need to strip them.

print("\n" + "=" * 70)
print("SECTION 3: RUNNING MAIN PIPELINE")
print("=" * 70)

# Read the main notebook file
main_file = "notebooks/ragatherapy_colab_cells.py"
with open(main_file, "r", encoding="utf-8") as f:
    main_code = f.read()

# Strip Colab-specific lines
lines = main_code.split('\n')
clean_lines = []
skip_patterns = [
    '!pip install',
    '!apt-get',
    'google.colab',
    'drive.mount',
]

for line in lines:
    stripped = line.strip()
    # Skip shell commands and colab imports
    if any(stripped.startswith(pat) for pat in skip_patterns):
        continue
    # Skip the imports we already did (avoid double import)
    if stripped.startswith('import pandas') and 'pd' in stripped:
        continue
    if stripped.startswith('import numpy') and 'np' in stripped:
        continue
    if stripped.startswith('import matplotlib') and 'plt' not in stripped:
        continue
    clean_lines.append(line)

# Find where Cell 4 starts (skip Cell 1 markdown, Cell 2 imports, Cell 3 downloads — we did those above)
cell4_marker = None
for i, line in enumerate(clean_lines):
    if 'CELL 4' in line and 'Raga Knowledge Base' in line:
        cell4_marker = i - 1  # include the === line before
        break

if cell4_marker is None:
    print("ERROR: Could not find Cell 4 marker. Running full file...")
    exec_code = '\n'.join(clean_lines)
else:
    # Run from Cell 4 onwards (Cells 4-18)
    exec_code = '\n'.join(clean_lines[cell4_marker:])

print(f"   Executing {len(exec_code.split(chr(10)))} lines from Cell 4 to Cell 18...")
print("   (This will take 5-15 minutes)\n")

# Execute in current namespace so variables persist
exec(exec_code, globals())

print("\n" + "=" * 70)
print("MAIN PIPELINE COMPLETE — RUNNING QUALITY FIXES")
print("=" * 70)

# ================================================================
# SECTION 4: Run publication enhancements
# ================================================================
pub_file = "notebooks/publication_enhancements.py"
if os.path.exists(pub_file):
    print(f"\n🔄 Running publication enhancements...")
    with open(pub_file, "r", encoding="utf-8") as f:
        pub_code = f.read()
    # Strip shell commands
    pub_lines = [l for l in pub_code.split('\n')
                 if not l.strip().startswith('!')]
    exec('\n'.join(pub_lines), globals())
    print("✅ Publication enhancements complete")
else:
    print(f"   ⚠ {pub_file} not found, skipping")

# ================================================================
# SECTION 5: Run quality fixes
# ================================================================
fix_file = "notebooks/quality_fixes.py"
if os.path.exists(fix_file):
    print(f"\n🔄 Running quality fixes...")
    with open(fix_file, "r", encoding="utf-8") as f:
        fix_code = f.read()
    fix_lines = [l for l in fix_code.split('\n')
                 if not l.strip().startswith('!')]
    exec('\n'.join(fix_lines), globals())
    print("✅ Quality fixes complete")
else:
    print(f"   ⚠ {fix_file} not found, skipping")

# ================================================================
# FINAL SUMMARY
# ================================================================
print("\n" + "=" * 70)
print("🎉 RAGATHERAPY — ALL SECTIONS COMPLETE!")
print("=" * 70)

print(f"""
📁 Output Files:
   data/knowledge_base/       → Raga KB (42 ragas), Disease Map (30 conditions)
   data/processed/            → Training data (~2,550 samples), independent labels
   models/recommendation/     → XGBoost, DNN, Autoencoder, Ensemble models
   models/nlp/                → TF-IDF, SBERT embeddings, fine-tuned SBERT
   reports/figures/           → 14+ publication-quality plots
   reports/metrics/           → Evaluation JSON files

📊 Key Metrics:
   Check reports/metrics/evaluation_metrics.json for all scores.

🖼  Figures saved to reports/figures/:
   - confusion_matrices.png
   - topk_accuracy.png
   - per_class_metrics.png
   - model_comparison.png
   - dnn_training.png
   - xgb_feature_importance.png
   - shap_summary.png
   - shap_importance.png
   - shap_waterfall.png
   - therapeutic_score_distribution.png
   - correlation_heatmap.png
   - top_ragas_by_condition.png
   - arousal_valence_space.png
   - raga_dendrogram.png
   - baseline_comparison.png

✅ Ready for paper writing!
""")
