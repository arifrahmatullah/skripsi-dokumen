import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse

fig, ax = plt.subplots(figsize=(12, 9))
ax.set_xlim(0, 12)
ax.set_ylim(0, 9)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('white')

# ── "uc UseCase" tab ─────────────────────────────────────────────────────────
ax.add_patch(FancyBboxPatch((1.4, 8.55), 1.5, 0.42,
    boxstyle='square,pad=0.04', lw=1.2,
    edgecolor='#555555', facecolor='#EEEEEE'))
ax.text(2.15, 8.76, 'uc UseCase', ha='center', va='center',
        fontsize=8, color='#333333')

# ── System boundary ───────────────────────────────────────────────────────────
ax.add_patch(FancyBboxPatch((1.4, 0.5), 10.1, 8.08,
    boxstyle='round,pad=0.05', lw=1.8,
    edgecolor='#555555', facecolor='white'))
ax.text(6.45, 8.35, 'Sistem Rekomendasi Tindak Lanjut\nKonfirmasi Pendaftaran Mahasiswa Baru',
        ha='center', va='center', fontsize=10.5, fontweight='bold', color='#111111')

# ── Stick figure ──────────────────────────────────────────────────────────────
def draw_actor(cx, cy, label):
    ax.add_patch(plt.Circle((cx, cy+0.95), 0.21,
                             color='#444444', fill=False, lw=1.8, zorder=6))
    ax.plot([cx, cx],           [cy+0.74, cy+0.18],  color='#444444', lw=1.8, zorder=6)
    ax.plot([cx-0.33, cx+0.33], [cy+0.53, cy+0.53],  color='#444444', lw=1.8, zorder=6)
    ax.plot([cx, cx-0.28],      [cy+0.18, cy-0.22],  color='#444444', lw=1.8, zorder=6)
    ax.plot([cx, cx+0.28],      [cy+0.18, cy-0.22],  color='#444444', lw=1.8, zorder=6)
    ax.text(cx, cy-0.48, label, ha='center', va='top',
            fontsize=10, fontweight='bold', color='#111111')

# ── Use case oval ─────────────────────────────────────────────────────────────
def draw_uc(cx, cy, text, w=2.9, h=0.60):
    ax.add_patch(Ellipse((cx, cy), w, h, lw=1.6,
                         edgecolor='#2255AA', facecolor='#D6E4F7', zorder=4))
    lines = text.split('\n')
    offset = 0.12 if len(lines) > 1 else 0
    for i, line in enumerate(lines):
        ax.text(cx, cy + offset - i*0.24, line,
                ha='center', va='center', fontsize=9,
                color='#111111', zorder=5)

# ── Line actor → use case ─────────────────────────────────────────────────────
def line(x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color='#444444', lw=1.3, zorder=3)

# =============================================================================
# ACTOR
# =============================================================================
draw_actor(0.55, 4.0, 'Tim\nMarketing')

# =============================================================================
# USE CASES — 7 use case tersebar merata secara vertikal
# =============================================================================
uc_x = 6.45
ucs = [
    (uc_x, 7.60, 'Login'),
    (uc_x, 6.55, 'Logout'),
    (uc_x, 5.50, 'Kelola Data\nPendaftar'),
    (uc_x, 4.40, 'Lihat Hasil Klasifikasi\nNaive Bayes'),
    (uc_x, 3.30, 'Lihat Rekomendasi\nTindak Lanjut'),
    (uc_x, 2.20, 'Lihat Detail\nHasil Prediksi'),
    (uc_x, 1.10, 'Cetak / Export\nLaporan'),
]

for (cx, cy, text) in ucs:
    draw_uc(cx, cy, text)

# =============================================================================
# KONEKSI aktor → tiap use case
# =============================================================================
ax_cx = 0.55 + 0.33   # kanan actor
ax_cy = 4.0 + 0.53    # tinggi lengan

for (cx, cy, _) in ucs:
    line(ax_cx, ax_cy, cx - 1.45, cy)

# =============================================================================
plt.tight_layout(pad=0.2)
plt.savefig('Use Case Diagram.png', dpi=180, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('Saved: Use Case Diagram.png')
plt.close()
