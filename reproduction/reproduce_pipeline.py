"""
RagaTherapy — Faithful re-implementation of the paper's methodology
(Section 4: Scoring Engine, Section 6: Experimental Setup)
Uses the exact 30-raga / 23-condition knowledge base from the project's
src/data/*.ts files (matches Appendix A and Appendix B in the manuscript).
"""
import json, random
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, top_k_accuracy_score
from sklearn.neural_network import MLPClassifier
import xgboost as xgb

RNG_SEED = 42
random.seed(RNG_SEED)
np.random.seed(RNG_SEED)

ragas = json.load(open('ragas_parsed.json'))
diseases = json.load(open('diseases_parsed.json'))

conditions = list(diseases.keys())
FEATS = ['stress_score', 'sleep_disruption', 'mood_score', 'relaxation_need',
          'emotional_stability_need', 'focus_need', 'energy_level', 'pain_level']

print(f"Loaded {len(ragas)} ragas, {len(conditions)} conditions")

# ================================================================
# Section 4: Scoring engine — exact formulas from the manuscript
# ================================================================
def score_raga(raga, P, detected_conditions):
    A_r = raga['arousal_level']; V_r = raga['valence']
    SR_r = raga['stress_reduction']; SI_r = raga['sleep_induction']
    PR_r = raga['pain_relief']; FE_r = raga['focus_enhancement']
    ES_r = raga['emotional_stability']; EV_r = raga['therapy_evidence_score']

    Relax = min((1/1.5) * (SR_r * P['relaxation_need'] + (1 - A_r) * P['stress_score']), 1.0)
    Emo = min((1/1.5) * (ES_r * P['emotional_stability_need'] + V_r * (1 - P['mood_score'])), 1.0)
    Evidence = EV_r
    Acoustic = (1/3.0) * (SI_r * P['sleep_disruption'] + PR_r * P['pain_level'] + FE_r * P['focus_need'])

    target_lower = [t.lower() for t in raga['target_conditions']]
    inter = sum(1 for c in detected_conditions if any(c in t or t in c for t in target_lower))
    CondSim = min(inter / max(len(detected_conditions), 1), 1.0)

    raw = 0.30*Relax + 0.25*Emo + 0.20*Evidence + 0.15*Acoustic + 0.10*CondSim

    contra_lower = [c.lower() for c in raga['contraindications']]
    has_contra = any(dc in cl or cl in dc for dc in detected_conditions for cl in contra_lower)
    return 0.0 if has_contra else raw

def best_raga_for_profile(P, detected_conditions):
    scores = [(r['raga_name'], score_raga(r, P, detected_conditions)) for r in ragas]
    scores.sort(key=lambda x: -x[1])
    return scores[0][0], scores

# ================================================================
# Section 6.2: Dataset Generation
# 12 base templates x 8 noise-injected variants per condition (96/condition)
# + 80 co-morbidity blended samples
# ================================================================
def make_templates(cond_feat, n=12):
    """12 base clinical feature templates per condition (small structured perturbations)."""
    templates = []
    base = np.array([cond_feat[f] for f in FEATS])
    # structured template variation: mild deterministic offsets to represent
    # different "typical symptom presentations"
    offsets = np.linspace(-0.06, 0.06, n)
    for i in range(n):
        t = np.clip(base + offsets[i] * np.array([1, -1, 1, -1, 1, -1, 1, -1]) * 0.5, 0, 1)
        templates.append(t)
    return templates

records = []
for cond in conditions:
    cond_feat = diseases[cond]
    templates = make_templates(cond_feat, n=12)
    for t in templates:
        for _ in range(8):  # 8 Gaussian-noise draws per template
            noisy = np.clip(t + np.random.normal(0, 0.05, size=len(FEATS)), 0, 1)
            P = dict(zip(FEATS, noisy))
            label, _ = best_raga_for_profile(P, [cond])
            rec = dict(zip(FEATS, noisy))
            rec['condition'] = cond
            rec['label'] = label
            records.append(rec)

print(f"Single-condition samples: {len(records)}")

# 80 co-morbidity samples: blend random condition pairs
for _ in range(80):
    c1, c2 = random.sample(conditions, 2)
    w = random.random()
    P = {f: w*diseases[c1][f] + (1-w)*diseases[c2][f] for f in FEATS}
    P = {f: np.clip(P[f] + np.random.normal(0, 0.03), 0, 1) for f in FEATS}
    label, _ = best_raga_for_profile(P, [c1, c2])
    rec = dict(P)
    rec['condition'] = f"{c1}+{c2}"
    rec['label'] = label
    records.append(rec)

df = pd.DataFrame(records)
print(f"Total dataset: {len(df)} samples")
print(f"Unique raga labels used: {df['label'].nunique()} / {len(ragas)}")
print("\nTop label distribution:")
print(df['label'].value_counts(normalize=True).head(5))

darbari_pct = (df['label'] == 'Darbari Kanada').mean() * 100
print(f"\nDarbari Kanada share: {darbari_pct:.2f}% (paper reports 53.97%)")

df.to_csv('synthetic_dataset.csv', index=False)

# ================================================================
# Section 6.3: Evaluation Paradigms
# ================================================================
X = df[FEATS].values
le = LabelEncoder()
y = le.fit_transform(df['label'])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RNG_SEED, stratify=y if pd.Series(y).value_counts().min() > 1 else None
)

# --- XGBoost (300 estimators, depth 8) ---
xgb_clf = xgb.XGBClassifier(n_estimators=300, max_depth=8, use_label_encoder=False,
                              eval_metric='mlogloss', random_state=RNG_SEED)
xgb_clf.fit(X_train, y_train)
xgb_pred = xgb_clf.predict(X_test)
xgb_proba = xgb_clf.predict_proba(X_test)
xgb_acc = accuracy_score(y_test, xgb_pred)
xgb_p, xgb_r, xgb_f1, _ = precision_recall_fscore_support(y_test, xgb_pred, average='macro', zero_division=0)
n_classes_test = len(np.unique(y_train))
try:
    xgb_top3 = top_k_accuracy_score(y_test, xgb_proba, k=3, labels=np.arange(xgb_proba.shape[1]))
except Exception:
    xgb_top3 = float('nan')

# --- MLP (128-256-128-64) ---
mlp_clf = MLPClassifier(hidden_layer_sizes=(128, 256, 128, 64), max_iter=500, random_state=RNG_SEED)
mlp_clf.fit(X_train, y_train)
mlp_pred = mlp_clf.predict(X_test)
mlp_proba = mlp_clf.predict_proba(X_test)
mlp_acc = accuracy_score(y_test, mlp_pred)
mlp_p, mlp_r, mlp_f1, _ = precision_recall_fscore_support(y_test, mlp_pred, average='macro', zero_division=0)
try:
    mlp_top3 = top_k_accuracy_score(y_test, mlp_proba, k=3, labels=np.arange(mlp_proba.shape[1]))
except Exception:
    mlp_top3 = float('nan')

# --- Majority baseline ---
majority_class = pd.Series(y_train).mode()[0]
maj_pred = np.full_like(y_test, majority_class)
maj_acc = accuracy_score(y_test, maj_pred)

print("\n" + "="*60)
print("IN-DISTRIBUTION RESULTS (paper reports: Majority 53.93%, MLP 84.93%, XGB 86.03%)")
print("="*60)
print(f"Majority Baseline : Acc={maj_acc:.4f}")
print(f"MLP               : Acc={mlp_acc:.4f}  P={mlp_p:.4f} R={mlp_r:.4f} F1={mlp_f1:.4f} Top3={mlp_top3:.4f}")
print(f"XGBoost           : Acc={xgb_acc:.4f}  P={xgb_p:.4f} R={xgb_r:.4f} F1={xgb_f1:.4f} Top3={xgb_top3:.4f}")

# ================================================================
# LOCO: Leave-One-Condition-Out
# ================================================================
print("\n" + "="*60)
print("LOCO CROSS-VALIDATION (paper reports mean 0.2935, range 0.0000-0.9583)")
print("="*60)

loco_results = {}
df_single = df[~df['condition'].str.contains(r'\+', regex=True)].copy()

for held_out in conditions:
    train_df = df_single[df_single['condition'] != held_out]
    test_df = df_single[df_single['condition'] == held_out]
    if len(test_df) == 0 or len(train_df) == 0:
        continue

    le_fold = LabelEncoder()
    le_fold.fit(train_df['label'])

    Xtr = train_df[FEATS].values
    ytr = le_fold.transform(train_df['label'])

    fold_clf = xgb.XGBClassifier(n_estimators=150, max_depth=6, use_label_encoder=False,
                                   eval_metric='mlogloss', random_state=RNG_SEED)
    fold_clf.fit(Xtr, ytr)

    Xte = test_df[FEATS].values
    y_true_labels = test_df['label'].values

    correct = 0
    for i in range(len(Xte)):
        true_label = y_true_labels[i]
        if true_label not in le_fold.classes_:
            correct += 0  # optimal raga never seen in training fold -> incorrect
            continue
        pred = fold_clf.predict(Xte[i:i+1])[0]
        pred_label = le_fold.inverse_transform([pred])[0]
        if pred_label == true_label:
            correct += 1
    acc = correct / len(Xte)
    loco_results[held_out] = (len(Xte), acc)
    print(f"  {held_out:20s} N={len(Xte):3d}  LOCO Acc={acc:.4f}")

mean_loco = np.mean([v[1] for v in loco_results.values()])
print(f"\nMean LOCO accuracy: {mean_loco:.4f}  (paper reports 0.2935)")
print(f"Range: {min(v[1] for v in loco_results.values()):.4f} - {max(v[1] for v in loco_results.values()):.4f}")

# Save everything
results_summary = {
    'in_distribution': {
        'majority': {'accuracy': maj_acc},
        'mlp': {'accuracy': mlp_acc, 'precision': mlp_p, 'recall': mlp_r, 'f1': mlp_f1, 'top3': mlp_top3},
        'xgboost': {'accuracy': xgb_acc, 'precision': xgb_p, 'recall': xgb_r, 'f1': xgb_f1, 'top3': xgb_top3},
    },
    'loco': {k: {'n': v[0], 'accuracy': v[1]} for k, v in loco_results.items()},
    'loco_mean': mean_loco,
    'darbari_kanada_share_pct': darbari_pct,
    'dataset_size': len(df),
}
json.dump(results_summary, open('reproduction_results.json', 'w'), indent=2)
print("\nSaved to reproduction_results.json")
