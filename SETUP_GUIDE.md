# RagaTherapy — Complete Setup Guide

## How to Run This Project

You have **3 options**:

---

## OPTION 1: Run on Local Desktop (Recommended First)

### Step 1: Install Python
- Install Python 3.9+ from https://python.org
- Verify: `python --version`

### Step 2: Create virtual environment
```bash
cd ragatherapy
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 3: Install all packages
```bash
pip install pandas numpy scikit-learn nltk sentence-transformers xgboost shap joblib matplotlib seaborn requests torch
```

**Note:** PyTorch install can be large (~2GB). For CPU-only (faster install):
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Step 4: Run the complete pipeline
```bash
python notebooks/run_local.py
```

This will:
- Create all directories
- Download all datasets
- Build the raga knowledge base (42 ragas)
- Run EDA and save figures
- Clean data
- Create disease-feature map (30 conditions)
- Run NLP pipeline
- Build recommendation engine
- Generate 2,550 augmented training samples
- Train XGBoost
- Run Sentence-BERT semantic NLP
- Train DNN + Autoencoder + Ensemble
- Run comprehensive evaluation with confusion matrices
- Run SHAP explainability
- Run interactive predictions
- Save all models
- Run quality fixes (honest evidence levels, SBERT fine-tuning, clustering)
- Print final summary

**Expected runtime:** 10-20 minutes (CPU), 5-10 minutes (GPU)

### Step 5: Check outputs
```
data/                          → All datasets
models/                        → All trained models (.pkl, .pt)
reports/figures/               → All charts and plots (14+ PNG files)
reports/metrics/               → All JSON metrics files
RAGATHERAPY_COMPLETE.txt       → Completion marker
```

---

## OPTION 2: Run on Google Colab

### Step 1: Open Google Colab
Go to https://colab.research.google.com

### Step 2: Upload the notebook
- Click **File → Upload notebook**
- Upload `notebooks/RagaTherapy.ipynb`

### Step 3: Enable GPU (Optional but faster)
- Click **Runtime → Change runtime type**
- Select **GPU** (T4)
- Click **Save**

### Step 4: Run all cells
- Click **Runtime → Run all**
- Or run each cell one by one with **Shift+Enter**

### Step 5: Download outputs
After all cells complete:
- Click the **Files** panel on the left
- Download `reports/figures/` folder for all plots
- Download `models/` folder for trained models
- Download `reports/metrics/` for evaluation JSON files

---

## OPTION 3: Run Cell-by-Cell (Manual)

If you prefer to understand each step:

### For Colab:
Copy each cell from `notebooks/ragatherapy_colab_cells.py` into separate Colab cells.
The file has `# CELL X` markers — each marker starts a new cell.

### For Local Jupyter:
```bash
pip install jupyterlab
jupyter lab
```
Then open `notebooks/RagaTherapy.ipynb`

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'sentence_transformers'"
```bash
pip install sentence-transformers
```

### "CUDA not available" warning
This is fine — the code runs on CPU too. GPU just makes it faster.

### "FileNotFoundError: symptom_disease_train.csv"
Check your internet connection. The script downloads this from GitHub.

### SHAP plot errors
SHAP sometimes has display issues. The plots are still saved to `reports/figures/` even if display fails.

### Out of memory
If you run out of RAM on Colab, use **Runtime → Change runtime type → High-RAM**.
On local desktop, close other applications.

---

## File Overview

```
notebooks/
├── RagaTherapy.ipynb              ← USE THIS for Colab (proper .ipynb)
├── run_local.py                   ← USE THIS for local desktop
├── ragatherapy_colab_cells.py     ← Raw cells (reference)
├── publication_enhancements.py    ← K-fold, baselines, ablation
├── quality_fixes.py               ← Evidence fixes, SBERT fine-tuning
└── ragatherapy_colab.py           ← Old version (reference)
```
