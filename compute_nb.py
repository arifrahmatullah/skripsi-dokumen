"""
Hitung Naive Bayes dari full dataset 1285 record.
Output: testing_results.json (dipakai insert_bab4.py)
"""
import json, math
import pandas as pd
from collections import defaultdict

# ─── Load & prepare ──────────────────────────────────────────────────────────
df = pd.read_excel('Data-Skirpsi.csv(1).xlsx')

FITUR = ['kategori_jarak_asal', 'tingkat_follow_up_internal',
         'status_test', 'kategori_nilai_test', 'kategori_penghasilan']
TARGET = 'status_retensi_final_target'
KELAS  = ['MASUK', 'TIDAK MASUK']

# Bersihkan nilai (ganti underscore → spasi agar konsisten tampilan)
for f in FITUR:
    df[f] = df[f].str.replace('_', ' ').str.strip()
df[TARGET] = df[TARGET].str.strip()

# ─── Split 80% train / 20% test (stratified) ─────────────────────────────────
from sklearn.model_selection import train_test_split
train_df, test_df = train_test_split(
    df, test_size=0.20, random_state=42, stratify=df[TARGET]
)
train_df = train_df.reset_index(drop=True)
test_df  = test_df.reset_index(drop=True)

N_TRAIN = len(train_df)
N_TEST  = len(test_df)
print(f"Train: {N_TRAIN}  |  Test: {N_TEST}")
print("Train class dist:", train_df[TARGET].value_counts().to_dict())
print("Test  class dist:", test_df[TARGET].value_counts().to_dict())

# ─── Prior Probability ────────────────────────────────────────────────────────
prior = {}
for k in KELAS:
    prior[k] = train_df[TARGET].value_counts()[k]

print(f"\nPrior: MASUK={prior['MASUK']}, TIDAK MASUK={prior['TIDAK MASUK']}, N={N_TRAIN}")

# ─── Conditional Probability dengan Laplace Smoothing ────────────────────────
cond = {}   # cond[fitur][kelas][nilai] = probability
for f in FITUR:
    cond[f] = {}
    unique_vals = sorted(df[f].dropna().unique())
    K = len(unique_vals)
    for k in KELAS:
        sub = train_df[train_df[TARGET] == k][f]
        n_k = len(sub)
        cond[f][k] = {}
        for v in unique_vals:
            ni = (sub == v).sum()
            cond[f][k][v] = (ni + 1) / (n_k + K)

# ─── Predict test set ────────────────────────────────────────────────────────
def predict(row):
    scores = {}
    for k in KELAS:
        n_k = prior[k]
        p_prior = n_k / N_TRAIN
        p = p_prior
        pm_parts = []
        for f in FITUR:
            v = row[f]
            prob = cond[f][k].get(v, 1 / (prior[k] + len(cond[f][k])))
            pm_parts.append(round(prob, 4))
            p *= prob
        scores[k] = (p, p_prior, pm_parts)
    return scores

results = []
for i, row in test_df.iterrows():
    sc = predict(row)
    post_m = round(sc['MASUK'][0], 8)
    post_t = round(sc['TIDAK MASUK'][0], 8)
    pred   = 'MASUK' if post_m >= post_t else 'TIDAK MASUK'
    aktual = row[TARGET]
    results.append({
        'nama'   : row['nama_pendaftar'].strip(),
        'vals'   : [row[f] for f in FITUR],
        'pm'     : sc['MASUK'][2],
        'pt'     : sc['TIDAK MASUK'][2],
        'prior_m': round(sc['MASUK'][1], 4),
        'prior_t': round(sc['TIDAK MASUK'][1], 4),
        'post_m' : post_m,
        'post_t' : post_t,
        'pred'   : pred,
        'aktual' : aktual,
    })

# ─── Confusion Matrix ─────────────────────────────────────────────────────────
tp = sum(1 for r in results if r['pred']=='MASUK'       and r['aktual']=='MASUK')
tn = sum(1 for r in results if r['pred']=='TIDAK MASUK' and r['aktual']=='TIDAK MASUK')
fp = sum(1 for r in results if r['pred']=='MASUK'       and r['aktual']=='TIDAK MASUK')
fn = sum(1 for r in results if r['pred']=='TIDAK MASUK' and r['aktual']=='MASUK')

total = tp + tn + fp + fn
acc   = round((tp + tn) / total * 100, 2)
prec  = round(tp / (tp + fp) * 100, 2) if (tp+fp) > 0 else 0
rec   = round(tp / (tp + fn) * 100, 2) if (tp+fn) > 0 else 0
f1    = round(2 * prec * rec / (prec + rec), 2) if (prec+rec) > 0 else 0

print(f"\nTP={tp}  TN={tn}  FP={fp}  FN={fn}")
print(f"Akurasi={acc}%  Presisi={prec}%  Recall={rec}%  F1={f1}%")

# ─── Cond prob tables untuk insert ke Word ───────────────────────────────────
# Format: {fitur: {kelas_m: {nilai: (ni, prob)}, kelas_t: {nilai: (ni, prob)}}}
cond_tables = {}
for f in FITUR:
    unique_vals = sorted(df[f].dropna().unique())
    K = len(unique_vals)
    cond_tables[f] = {'vals': unique_vals, 'K': K}
    for k in KELAS:
        sub = train_df[train_df[TARGET] == k][f]
        n_k = len(sub)
        rows_k = {}
        for v in unique_vals:
            ni = int((sub == v).sum())
            prob = round((ni + 1) / (n_k + K), 4)
            rows_k[v] = {'ni': ni, 'n': n_k, 'prob': prob,
                         'frac': f'({ni}+1)/({n_k}+{K})'}
        cond_tables[f][k] = rows_k

# ─── Training rows (untuk tabel di Word) ─────────────────────────────────────
train_rows = []
for i, row in train_df.iterrows():
    train_rows.append({
        'no'   : i + 1,
        'nama' : row['nama_pendaftar'].strip(),
        'vals' : [row[f] for f in FITUR],
        'kelas': row[TARGET],
    })

# ─── Save JSON ────────────────────────────────────────────────────────────────
out = {
    'n_train' : N_TRAIN,
    'n_test'  : N_TEST,
    'prior'   : {k: {'n': prior[k], 'prob': round(prior[k]/N_TRAIN, 4)} for k in KELAS},
    'cond_tables': cond_tables,
    'results' : results,
    'train_rows': train_rows,
    'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn,
    'acc': acc, 'prec': prec, 'rec': rec, 'f1': f1,
}
import numpy as np
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)): return int(obj)
        if isinstance(obj, (np.floating,)): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        return super().default(obj)

with open('testing_results.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2, cls=NpEncoder)
print("\nSaved testing_results.json")
